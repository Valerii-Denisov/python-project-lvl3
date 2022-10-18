"""The module contains functions for name and path of web pages element."""

import os
import re
from urllib import parse as parser


def get_folder_name(raw_address):
    """
    Build folder name.

    Parameters:
        raw_address: string.

    Returns:
          Folder name.
    """
    url_data = parser.urlparse(raw_address)
    raw_name = '{0}{1}'.format(url_data.netloc, url_data.path)
    name = re.sub(r'(/|[.])', '-', raw_name)
    return '{0}{1}'.format(name, '_files')


def get_file_name(raw_address):
    """
    разбить на две функции: одна под имена файлов другая под имена директорий
    Build file name.

    Parameters:
        raw_address: string.

    Returns:
          File name.
    """
    url_data = parser.urlparse(raw_address)
    raw_name = '{0}{1}'.format(url_data.netloc, url_data.path)
    _, file_format = os.path.splitext(raw_address)
    name = re.sub(r'(/|[.])', '-', raw_name)
    if re.search(r'css$', name):
        return '{0}{1}'.format(
            re.search(r'[a-zA-Z\d-]*(?=-css)', name).group(),
            file_format,
        )
    elif re.search(r'(png|jpg)$', name):
        return '{0}{1}'.format(
            re.search(r'[a-zA-Z\d-]*(?=-jpg|-png)', name).group(),
            file_format,
        )
    elif re.search(r'js$', name):
        return '{0}{1}'.format(
            re.search(r'[a-zA-Z\d-]*(?=-js)', name).group(),
            file_format,
        )
    return '{0}{1}'.format(re.search(r'[a-zA-Z\d-]*', name).group(), '.html')
