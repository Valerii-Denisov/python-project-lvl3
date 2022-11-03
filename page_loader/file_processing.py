"""The module contains the functions for making files and directory's."""

import logging
import os

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
        log_pars.debug(
            "Can't write to directory. Error: {0}".format(error_one),
        )
        raise error_one
    except FileNotFoundError as error_two:
        log_pars.debug(
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
