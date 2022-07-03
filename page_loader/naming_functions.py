"""The module contains functions for name and path of web pages element."""

import logging
import os
import re
from urllib import parse as parser

from page_loader.module_dict import CONTENT_TYPE, FILE_FORMAT

log_pars = logging.getLogger('app_logger')


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
        return '{0}{1}'.format(
            element_name.group(),
            get_file_format(url_data.path, object_type),
        )
    return '{0}{1}'.format(name, get_file_format(url_data.path, object_type))


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


def get_file_format(path, object_type):
    """
    Get file format.

    Parameters:
        path: string;
        object_type: string.

    Returns:
          file_format: string.
    """
    _, file_format = os.path.splitext(path)
    if file_format:
        return file_format
    return FILE_FORMAT[object_type]
