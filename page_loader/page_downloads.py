"""The module contains the main functions for downloading web pages."""

import logging
import os
import re
import sys
from urllib import parse as parser

import requests
from bs4 import BeautifulSoup
from page_loader.module_dict import CONTENT_TYPE, FILE_FORMAT

log_pars = logging.getLogger('app_logger')


def page_download(url, local_path):
    """
    Save web page data to a local directory.

    Parameters:
        url: string;
        local_path: string

    Returns:
        Full path to saved contents.
    """
    directory_path = get_path(url, local_path, 'directory')
    make_directory(directory_path)
    page_content = requests.get(url).text
    for key in CONTENT_TYPE.keys():
        log_pars.info('Start download {0} element.'.format(key))
        page_content = save_content(
            page_content,
            parser.urlparse(url).netloc,
            directory_path,
            key,
        )
    html_file_path = get_path(url, local_path, 'html_page')
    with open(html_file_path, 'w') as write_file:
        write_file.write(page_content)
    return html_file_path


def get_name(raw_address, object_type, home_netloc=''):
    """
    Build file name.

    Parameters:
        raw_address: string;
        object_type: string;
        home_netloc: string.

    Returns:
          File name.
    """
    url_data = parser.urlparse(raw_address)
    if url_data.netloc:
        raw_name = '{0}{1}'.format(url_data.netloc, url_data.path)
    else:
        raw_name = '{0}{1}'.format(home_netloc, url_data.path)
    name = re.sub(r'(/|[.])', '-', raw_name)
    if object_type in CONTENT_TYPE.keys():
        element_name = re.search(
            r'[a-zA-Z\d-]*{0}'.format(
                CONTENT_TYPE[object_type]['name_pattern'],
            ),
            name,
        )
        return element_name.group() + FILE_FORMAT[object_type]
    return name + FILE_FORMAT[object_type]


def find_some(html_file, tag, resource_link):
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


def make_directory(path):
    """
    Create a directory on the specified path.

    Parameters:
        path: string.
    """
    try:
        if not os.path.isdir(path):
            os.mkdir(path)
    except FileNotFoundError as error:
        log_pars.error(error)
        sys.exit(1)


def get_path(url, local_path, source_type):
    """
    Build the full path of the element.

    Parameters:
        url: string,
        local_path: string,
        source_type: string.

    Returns:
          Path to element.
    """
    return os.path.join(local_path, get_name(url, source_type))


def save_content(content, home_netloc, directory, resource_type):
    """
    Save items from the specified list.

    Parameters:
        content: string;
        home_netloc: string;
        directory: string;
        resource_type: string.

    Returns:
          String.
    """
    result = content
    for element in find_some(
        result,
        CONTENT_TYPE[resource_type]['tag'],
        CONTENT_TYPE[resource_type]['linc'],
    ):
        if re.search(
            CONTENT_TYPE[resource_type]['pattern'],
            element[CONTENT_TYPE[resource_type].get('linc')],
        ):
            object_url_data = parser.urlparse(
                element[CONTENT_TYPE[resource_type]['linc']],
            )
            if object_url_data.netloc in {'', home_netloc}:
                name = get_name(
                    element[CONTENT_TYPE[resource_type]['linc']],
                    resource_type,
                    home_netloc,
                )
                element_local_path = '{0}/{1}'.format(directory, name)
                element_url = 'https://{0}{1}'.format(
                    home_netloc,
                    object_url_data.path,
                )
                with open(
                    element_local_path,
                    CONTENT_TYPE[resource_type]['write'],
                ) as write_file:
                    write_file.write(requests.get(element_url).content)
                result = re.sub(
                    element[CONTENT_TYPE[resource_type]['linc']],
                    os.path.join(os.path.split(directory)[1], name),
                    result,
                )
    return result
