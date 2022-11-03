"""The module contains the main functions for working with content."""
import os
import re
from urllib import parse as parser

import requests
from page_loader.url_functions import log_pars


def get_raw_data(url):
    """
    Load data from URL-address.

    Parameters:
        url: string.

    Raises:
        error_one: requests.exceptions.HTTPError,
        error_two: requests.exceptions.ConnectionError,
        error_three: requests.exceptions.Timeout.

    Returns:
          Raw page data.
    """
    try:
        raw_data = requests.get(url)
        raw_data.raise_for_status()
    except requests.exceptions.HTTPError as error_one:
        log_pars.debug('The item cannot be loaded. Find HTTP error')
        raise error_one
    except requests.exceptions.ConnectionError as error_two:
        log_pars.debug('The connection cannot be established.')
        raise error_two
    except requests.exceptions.Timeout as error_three:
        log_pars.debug('The time for connection is over.')
        raise error_three
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
    if element:
        resource_netloc = parser.urlparse(element).netloc
        base_netloc = parser.urlparse(base_url).netloc
        return resource_netloc in {'', base_netloc}


def get_local_content(page_soup, tag, link, base_url):
    """
    Build a list of local elements.

    Parameters:
        page_soup: string,
        tag: string,
        link: string,
        base_url: string.

    Returns:
          Resource list.
    """
    result = []
    for element in page_soup.find_all(tag):
        if is_local_content(element.get(link), base_url):
            element_file_format = element[link].split('.')[-1]
            if element_file_format in {'jpg', 'png', 'css', 'js', 'html'}:
                result.append(element)
            elif re.search(r'^(?!.*css).', element[link]):
                result.append(element)
    return result


def get_element_attributes(resource_tag):
    """
    Return attributes of HTML element.

    Parameters:
        resource_tag: string.

    Returns:
        link: string.
    """
    if resource_tag in {'img', 'script'}:
        link = 'src'
    else:
        link = 'href'
    return link


def replace_source_link(element, directory, name, link):
    """
    Replace resource references with local ones.

    Parameters:
         element: tag;
         name: string;
         directory: string;
         link: string.
    """
    element[link] = os.path.join(
        os.path.split(directory)[1],
        name,
    )
