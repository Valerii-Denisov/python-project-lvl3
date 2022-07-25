"""The module contains the functions for making files and directory's."""

import logging
import os
from urllib import parse as parser

from page_loader.module_dict import CONTENT_TYPE
from page_loader.naming_functions import get_name
from page_loader.url_functions import get_local_content, get_raw_data
from progress.bar import Bar

log_pars = logging.getLogger('app_logger')


def make_directory(path):
    """
    Create a directory on the specified path.

    Parameters:
        path: string.

    Raises:
        PermissionError: error_one,
        FileNotFoundError: error_two.
    """
    try:
        if not os.path.isdir(path):
            os.mkdir(path)
    except PermissionError as error_one:
        log_pars.error(
            'Can not write to directory. Error: {0}'.format(error_one),
        )
        raise error_one
    except FileNotFoundError as error_two:
        log_pars.error(
            'Target directory not found. Error: {0}'.format(error_two),
        )
        raise error_two


def save_content(content, parsing_url, directory, resource_type):
    """
    Save items from the specified list.

    Parameters:
        content: string;
        parsing_url: string;
        directory: string;
        resource_type: string.

    Returns:
          String.
    """
    result = content
    element_list = get_local_content(result, resource_type, parsing_url.netloc)
    bar = Bar('Download: ', max=len(element_list))
    for element in element_list:
        object_url_data = parser.urlparse(
            element[CONTENT_TYPE[resource_type]['linc']],
        )
        name = get_name(
                element[CONTENT_TYPE[resource_type]['linc']],
                resource_type,
                parsing_url.netloc,
            )
        element_local_path = '{0}/{1}'.format(directory, name)
        element_url = '{2}://{0}{1}'.format(
                parsing_url.netloc,
                object_url_data.path,
                parsing_url.scheme,
            )
        write_to_file(
                element_local_path,
                resource_type,
                get_raw_data(element_url).content,
            )
        element[CONTENT_TYPE[resource_type]['linc']] = os.path.join(
                os.path.split(directory)[1],
                name,
            )
        bar.next()
    bar.finish()
    return result


def write_to_file(path, resource_type, content):
    """
    Save items from the specified list.

    Parameters:
        path:string;
        content: string;
        resource_type: string.
    """
    with open(
        path,
        CONTENT_TYPE[resource_type]['write'],
    ) as write_file:
        write_file.write(content)
