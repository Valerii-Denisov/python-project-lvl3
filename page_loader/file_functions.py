"""The module contains the functions for making files and directory's."""

import logging
import os

from page_loader.module_dict import CONTENT_TYPE_TAGS

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
        log_pars.exception(
            "Can't write to directory. Error: {0}".format(error_one),
        )
        raise error_one
    except FileNotFoundError as error_two:
        log_pars.exception(
            'Target directory not found. Error: {0}'.format(error_two),
        )
        raise error_two


def write_to_file(path, content):
    """
    Write data from file.

    Parameters:
        path:string;
        content: string.
    """
    with open(path, 'wb') as write_file:
        write_file.write(content)


def replace_source_link(element, directory, name, resource_type):
    """
    Replace resource references with local ones.

    Parameters:
         element: tag;
         name: string;
         directory: string;
         resource_type: string.
    """
    element[CONTENT_TYPE_TAGS[resource_type]['linc']] = os.path.join(
        os.path.split(directory)[1],
        name,
    )
