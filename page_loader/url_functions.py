"""The module contains the main functions for downloading web pages."""

import logging
import re
from urllib import parse as parser

import requests

log_pars = logging.getLogger('app_logger')


def get_raw_data(url):
    """
    Load data from URL-address.

    Parameters:
        url: string.

    Raises:
        error_one: requests.exceptions.HTTPError,
        error_two: requests.exceptions.ConnectionError.

    Returns:
          Raw page data.
    """
    try:
        raw_data = requests.get(url)
        raw_data.raise_for_status()
    except requests.exceptions.HTTPError as error_one:
        log_pars.error(
            'The page cannot be loaded.\nError: {0}'.format(
                error_one,
            ),
        )
        raise error_one
    except requests.exceptions.ConnectionError as error_two:
        log_pars.error(
            'The connection cannot be established. {0}'.format(error_two),
        )
        raise error_two
    return raw_data


def is_local_content(element, base_url):
    """
    переписать через проверку нетлока у юрла ресурса и юрла корневой страницы
    Check whether the resource is local or not.

    Parameters:
        element: bs4.element.Tag,
        base_url: string.

    Returns:
          True or false.
    """
    resource_netloc = parser.urlparse(element).netloc
    base_netloc = parser.urlparse(base_url).netloc
    return resource_netloc in {'', base_netloc}


def get_local_content(page_soup, tag, pattern, linc, base_url):
    """
    Build a list of local elements.

    Parameters:
        page_soup: string,
        tag: string,
        pattern: string,
        linc: string,
        base_url: string.

    Returns:
          Resource list.
    """
    result = []
    for element in page_soup.find_all(tag):
        if re.search(
            pattern,
            element[linc],
        ):
            if is_local_content(
                element[linc],
                base_url,
            ):
                result.append(element)
    return result


def get_source_url(parsing_url, element, linc):
    """
    Build the url of the element.

    Parameters:
        element: tag;
        parsing_url: string;
        linc: string.

    Returns:
          URL-address.
    """
    object_url_data = parser.urlparse(
        element[linc],
    )
    return '{2}://{0}{1}'.format(
        parsing_url.netloc,
        object_url_data.path,
        parsing_url.scheme,
    )


def get_url_with_netloc(raw_address, home_netloc):
    """
    Build full url.

    Parameters:
        raw_address: string;
        home_netloc: string.

    Returns:
          File name.
    """
    url_data = parser.urlparse(raw_address)
    if url_data.netloc:
        raw_url = '{0}{1}'.format(url_data.netloc, url_data.path)
    else:
        raw_url = '{0}{1}'.format(home_netloc, url_data.path)
    return raw_url


def get_element_attributes(resource_type):
    """
    Return attributes of HTML element.

    Parameters:
        resource_type: string.

    Returns:
        tag: string,
        pattern: string,
        linc: string.
    """
    if resource_type == 'images':
        tag = 'img'
        pattern = r'png|jpg'
        linc = 'src'
    elif resource_type == 'css':
        tag = 'link'
        pattern = r'css'
        linc = 'href'
    elif resource_type == 'script':
        tag = 'script'
        pattern = r'js'
        linc = 'src'
    else:
        tag = 'link'
        pattern = r'^(?!.*css).|html'
        linc = 'href'
    return tag, pattern, linc
