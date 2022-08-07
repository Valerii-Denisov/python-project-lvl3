"""The module contains the main functions for downloading web pages."""

import logging
from urllib import parse as parser

from bs4 import BeautifulSoup
from page_loader.file_functions import make_directory, save_content
from page_loader.module_dict import CONTENT_TYPE_TAGS
from page_loader.naming_functions import get_path
from page_loader.url_functions import get_raw_data

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
    target_directory_path = get_path(saving_url, local_path, 'directory')
    make_directory(target_directory_path)
    for content_tag in CONTENT_TYPE_TAGS.keys():
        page_html_tree = save_content(
            page_html_tree,
            parser.urlparse(saving_url),
            target_directory_path,
            content_tag,
        )
    html_file_path = get_path(saving_url, local_path, 'html_page')
    with open(html_file_path, 'w') as write_file:
        write_file.write(page_html_tree.prettify())
    return html_file_path
