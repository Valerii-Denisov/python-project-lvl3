"""The module contains the main functions for downloading web pages."""

import logging
import re
from urllib import parse as parser

import requests
from page_loader.module_dict import CONTENT_TYPE_TAGS

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


def get_local_content(page_soup, resource_type, base_url):
    """
    Build a list of local elements.

    Parameters:
        page_soup: string,
        resource_type: string,
        base_url: string.

    Returns:
          Resource list.
    """
    result = []
    for element in page_soup.find_all(CONTENT_TYPE_TAGS[resource_type]['tag']):
        if re.search(
            CONTENT_TYPE_TAGS[resource_type]['pattern'],
            element[CONTENT_TYPE_TAGS[resource_type]['linc']],
        ):
            if is_local_content(
                element[CONTENT_TYPE_TAGS[resource_type]['linc']],
                base_url,
            ):
                result.append(element)
    return result


def get_source_url(parsing_url, element, resource_type):
    """
    Build the url of the element.

    Parameters:
        element: tag;
        parsing_url: string;
        resource_type: string.

    Returns:
          URL-address.
    """
    object_url_data = parser.urlparse(
        element[CONTENT_TYPE_TAGS[resource_type]['linc']],
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
