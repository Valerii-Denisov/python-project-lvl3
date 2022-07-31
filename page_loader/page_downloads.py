"""The module contains the main functions for downloading web pages."""

import logging
from urllib import parse as parser

from bs4 import BeautifulSoup
from page_loader.file_functions import make_directory, save_content
from page_loader.module_dict import CONTENT_TYPE
from page_loader.naming_functions import get_path
from page_loader.url_functions import get_raw_data

log_pars = logging.getLogger('app_logger')


def download(url, local_path):
    """
    Save web page data to a local directory.

    Parameters:
        url: string;
        local_path: string

    Returns:
        Full path to saved contents.
    """
    page_content = BeautifulSoup(get_raw_data(url).text, 'html.parser')
    directory_path = get_path(url, local_path, 'directory')
    make_directory(directory_path)
    for key in CONTENT_TYPE.keys():
        page_content = save_content(
            page_content,
            parser.urlparse(url),
            directory_path,
            key,
        )
    html_file_path = get_path(url, local_path, 'html_page')
    with open(html_file_path, 'w') as write_file:
        write_file.write(page_content.prettify())
    return html_file_path
