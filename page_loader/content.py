"""The module contains the main functions for working with content."""
import logging
import re
from urllib import parse as parser

import requests

log_pars = logging.getLogger('app_logger')


def get_response(url):
    """
    Get a response to the HTTP-request.

    Parameters:
        url: string.

    Raises:
        error_one: requests.exceptions.HTTPError,
        error_two: requests.exceptions.ConnectionError,
        error_three: requests.exceptions.Timeout.

    Returns:
          Response object.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error_one:
        log_pars.error('The item cannot be loaded. HTTP error found.')
        raise error_one
    except requests.exceptions.ConnectionError as error_two:
        log_pars.error('The connection cannot be established.')
        raise error_two
    except requests.exceptions.Timeout as error_three:
        log_pars.error('The time for connection is over.')
        raise error_three
    return response


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


def get_local_content_tags(page_soup, tag, link, base_url):
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


def get_attribute_name(resource_tag):
    """
    Return name of the attribute containing the URL of the element.

    Parameters:
        resource_tag: string.

    Returns:
        attribute_name: string.
    """
    if resource_tag in {'img', 'script'}:
        attribute_name = 'src'
    else:
        attribute_name = 'href'
    return attribute_name
