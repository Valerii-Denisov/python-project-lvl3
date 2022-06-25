"""The module contains the functions for making files and directory's."""

import logging
import os
import re
import sys
from urllib import parse as parser

from page_loader.module_dict import CONTENT_TYPE
from page_loader.naming_functions import get_name
from page_loader.url_functions import find_local, find_some, get_raw_data
from progress.bar import Bar

log_pars = logging.getLogger('app_logger')


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
    element_list = find_local(
        find_some(
            result,
            CONTENT_TYPE[resource_type]['tag'],
            CONTENT_TYPE[resource_type]['linc'],
        ),
        resource_type,
    )
    bar = Bar('Download: ', max=len(element_list))
    for element in element_list:
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
                write_file.write(get_raw_data(element_url).content)
            result = re.sub(
                element[CONTENT_TYPE[resource_type]['linc']],
                os.path.join(os.path.split(directory)[1], name),
                result,
            )
            bar.next()
    bar.finish()
    return result
