"""The module contains the main functions for downloading web pages."""

import logging
import os
from urllib import parse as parser

import requests
from bs4 import BeautifulSoup
from page_loader.file_functions import (
    make_directory,
    replace_source_link,
    write_to_file,
)
from page_loader.naming_functions import get_file_name, get_folder_name
from page_loader.url_functions import (
    get_element_attributes,
    get_local_content,
    get_raw_data,
    get_source_url,
    get_url_with_netloc,
)
from progress.bar import Bar

log_pars = logging.getLogger('app_logger')


def download(saving_url, local_path):
    """
    Save web page data to a local directory.

    Parameters:
        saving_url: string;
        local_path: string

    Returns:
        Full path to saved contents.
    """
    page_html_tree = BeautifulSoup(get_raw_data(saving_url).text, 'html.parser')
    target_directory_path = os.path.join(
        local_path,
        get_folder_name(saving_url),
    )
    make_directory(target_directory_path)
    for content_type in ('img', 'script', 'link'):
        linc = get_element_attributes(content_type)
        element_list = get_local_content(
            page_html_tree,
            content_type,
            linc,
            saving_url,
        )
        bar = Bar(
            'Start download {0} content. Download: '.format(content_type),
            max=len(element_list),
        )
        for element in element_list:
            log_pars.info('Trying to download the item: {0}'.format(
                element[linc],
            ))
            full_url = get_url_with_netloc(
                element[linc],
                parser.urlparse(saving_url).netloc,
            )
            name = get_file_name(full_url)
            element_local_path = '{0}/{1}'.format(target_directory_path, name)
            element_url = get_source_url(
                parser.urlparse(saving_url),
                element,
                linc,
            )
            try:
                content = get_raw_data(element_url).content
            except requests.exceptions.RequestException as error_one:
                log_pars.warning(
                    'The item cannot be loaded.\nError: {0}'.format(
                        error_one,
                    ),
                )
            else:
                write_to_file(element_local_path, content)
                replace_source_link(
                    element,
                    target_directory_path,
                    name,
                    linc,
                )
            bar.next()
            log_pars.info('The item is downloaded.')
        bar.finish()
    html_file_path = os.path.join(local_path, get_file_name(saving_url))
    with open(html_file_path, 'w') as write_file:
        write_file.write(page_html_tree.prettify())
    return html_file_path
