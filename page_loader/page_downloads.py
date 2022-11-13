"""The module contains the main functions for downloading web pages."""

import logging
import os
from urllib import parse as parser

import requests
from bs4 import BeautifulSoup
from page_loader.content import (
    get_attribute_name,
    get_local_content_tags,
    get_response,
)
from page_loader.file import make_directory, write_to_file
from page_loader.naming import get_file_name, get_folder_name
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
    page_html_tree = BeautifulSoup(get_response(saving_url).text, 'html.parser')
    target_directory_path = os.path.join(
        local_path,
        get_folder_name(saving_url),
    )
    make_directory(target_directory_path)
    for content_type in ('img', 'script', 'link'):
        source_attribute_name = get_attribute_name(content_type)
        local_tags = get_local_content_tags(
            page_html_tree,
            content_type,
            source_attribute_name,
            saving_url,
        )
        bar = Bar(
            'Start download {0} content. Download: '.format(content_type),
            max=len(local_tags),
        )
        for tag in local_tags:
            log_pars.info('Trying to download the item: {0}'.format(
                tag[source_attribute_name],
            ))
            element_url = parser.urljoin(saving_url, tag[source_attribute_name])
            name = get_file_name(element_url)
            element_local_path = '{0}/{1}'.format(target_directory_path, name)
            try:
                content = get_response(element_url).content
            except requests.exceptions.RequestException as error_one:
                log_pars.warning(
                    'WARNING! The item cannot be loaded.\nError: {0}'.format(
                        error_one,
                    ),
                )
            else:
                write_to_file(element_local_path, content)
                tag[source_attribute_name] = os.path.join(
                    os.path.split(target_directory_path)[1],
                    name,
                )
                log_pars.info('The item is downloaded.')
                bar.next()
        bar.finish()
    html_file_path = os.path.join(local_path, get_file_name(saving_url))
    with open(html_file_path, 'w') as write_file:
        write_file.write(page_html_tree.prettify())
    return html_file_path
