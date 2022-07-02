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
        return element_name.group() + get_suffix(url_data.path, object_type)
    return name + get_suffix(url_data.path, object_type)


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


def get_suffix(path, object_type):
    """
    Get file suffix.

    Parameters:
        path: string;
        object_type: string.

    Returns:
          suffix.
    """
    _, suffix = os.path.splitext(path)
    if suffix:
        return suffix
    return FILE_FORMAT[object_type]
