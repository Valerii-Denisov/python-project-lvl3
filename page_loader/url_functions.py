"""The module contains the main functions for downloading web pages."""

import logging
import re
from urllib import parse as parser

import requests
from bs4 import BeautifulSoup
from page_loader.module_dict import CONTENT_TYPE

log_pars = logging.getLogger('app_logger')


def get_raw_data(url):
    """
    Load data from page.

    Parameters:
        url: string.

    Raises:
        error_one: requests.exceptions.HTTPError,
        error_two: requests.exceptions.ConnectionError.

    Returns:
          Page data.
    """
    try:
        raw_data = requests.get(url)
        raw_data.raise_for_status()
    except requests.exceptions.HTTPError as error_one:
        log_pars.error(
            'The page cannot be loaded.\nError code: {0}'.format(
                raw_data.status_code,
            ),
        )
        raise error_one
    except requests.exceptions.ConnectionError as error_two:
        log_pars.error(
            'The connection cannot be established.\nError: {0}'.format(
                error_two,
            ),
        )
        raise error_two
    return raw_data


def find_tag_content(html_file, tag, resource_link):
    """
    Find content from web page.

    Parameters:
        html_file: string;
        tag: string;
        resource_link: string.

    Returns:
          List of elements.
    """
    result_list = []
    soup = BeautifulSoup(html_file, 'html.parser')
    for element in soup.find_all(tag):
        if resource_link in element.attrs.keys():
            result_list.append(element)
    return result_list


def find_local_content(raw_list, resource_type, home_netloc):
    """
    Build dict is local element.

    Parameters:
        raw_list: list,
        resource_type: string.

    Returns:
          Resource list.
    """
    result = []
    for element in raw_list:
        if re.search(
            CONTENT_TYPE[resource_type]['pattern'],
            element[CONTENT_TYPE[resource_type]['linc']],
        ):
            object_url_data = parser.urlparse(
                element[CONTENT_TYPE[resource_type]['linc']],
            )
            if object_url_data.netloc in {'', home_netloc}:
                result.append(element)
    return result
