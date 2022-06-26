"""The module contains the main functions for downloading web pages."""

import logging
import sys
from urllib import parse as parser

import requests.exceptions
from page_loader.file_functions import make_directory, save_content
from page_loader.module_dict import CONTENT_TYPE
from page_loader.naming_functions import get_path
from page_loader.url_functions import get_raw_data

log_pars = logging.getLogger('app_logger')


def download(url, local_path):
    """
    Save web page data to a local directory.

    Parameters:
        url: string;
        local_path: string

    Returns:
        Full path to saved contents.
    """
    directory_path = get_path(url, local_path, 'directory')
    try:
        make_directory(directory_path)
    except FileNotFoundError:
        sys.exit(1)
    except PermissionError:
        sys.exit(1)
    try:
        page_content = get_raw_data(url).text
    except requests.exceptions.RequestException:
        sys.exit(1)
    for key in CONTENT_TYPE.keys():
        log_pars.info('Start download {0} element.'.format(key))
        page_content = save_content(
            page_content,
            parser.urlparse(url),
            directory_path,
            key,
        )
    html_file_path = get_path(url, local_path, 'html_page')
    with open(html_file_path, 'w') as write_file:
        write_file.write(page_content)
    return html_file_path
