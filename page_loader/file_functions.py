"""The module contains the functions for making files and directory's."""

import logging
import os

from page_loader.module_dict import CONTENT_TYPE_TAGS
from page_loader.naming_functions import get_name
from page_loader.url_functions import (
    get_local_content,
    get_raw_data,
    get_source_url,
)
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
        log_pars.exception(
            "Can't write to directory. Error: {0}".format(error_one),
        )
        raise error_one
    except FileNotFoundError as error_two:
        log_pars.exception(
            'Target directory not found. Error: {0}'.format(error_two),
        )
        raise error_two


def save_content(page_soup, parsing_url, directory, resource_type):
    """
    упразднить, весь функционал в донвлоад перенести (первоочередное остальные замечания завзаны на это
    Save items from the specified list.

    Parameters:
        page_soup: string;
        parsing_url: string;
        directory: string;
        resource_type: string.

    Returns:
          String.
    """
    element_list = get_local_content(
        page_soup,
        resource_type,
        parsing_url.netloc,
    )
    bar = Bar(
        'Start download {0} content. Download: '.format(resource_type),
        max=len(element_list),
    )
    for element in element_list:
        log_pars.info('Trying to download the item: {0}'.format(
            element[CONTENT_TYPE_TAGS[resource_type]['linc']],
        ))
        name = get_name(
            element[CONTENT_TYPE_TAGS[resource_type]['linc']],
            resource_type,
            parsing_url.netloc,
        )
        element_local_path = '{0}/{1}'.format(directory, name)
        element_url = get_source_url(parsing_url, element, resource_type)
        write_to_file(
            element_local_path,
            get_raw_data(element_url).content,
            resource_type,
        )
        replace_source_link(element, directory, name, resource_type)
        bar.next()
        log_pars.info('The item is downloaded.')
    bar.finish()
    return page_soup


def write_to_file(path, content, resource_type):
    """
    Write data from file.

    Parameters:
        path:string;
        content: string;
        resource_type: string.
    """
    with open(path, CONTENT_TYPE_TAGS[resource_type]['write']) as write_file:
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
