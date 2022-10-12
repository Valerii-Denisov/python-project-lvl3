"""The module contains the main functions for downloading web pages."""

import logging
from urllib import parse as parser

from bs4 import BeautifulSoup
from page_loader.file_functions import (
    make_directory,
    replace_source_link,
    write_to_file,
)
from page_loader.module_dict import CONTENT_TYPE_TAGS
from page_loader.naming_functions import (
    get_name,
    get_path,
    get_url_with_netloc,
)
from page_loader.url_functions import (
    get_local_content,
    get_raw_data,
    get_source_url,
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
    target_directory_path = get_path(saving_url, local_path, 'directory')
    make_directory(target_directory_path)
    for content_tag in CONTENT_TYPE_TAGS.keys():
        element_list = get_local_content(
            page_html_tree,
            content_tag,
            saving_url,
        )
        bar = Bar(
            'Start download {0} content. Download: '.format(content_tag),
            max=len(element_list),
        )
        for element in element_list:
            log_pars.info('Trying to download the item: {0}'.format(
                element[CONTENT_TYPE_TAGS[content_tag]['linc']],
            ))
            full_url = get_url_with_netloc(
                element[CONTENT_TYPE_TAGS[content_tag]['linc']],
                parser.urlparse(saving_url).netloc,
            )
            name = get_name(
                full_url,
                content_tag,
            )
            element_local_path = '{0}/{1}'.format(target_directory_path, name)
            element_url = get_source_url(
                parser.urlparse(saving_url),
                element,
                content_tag,
            )
            write_to_file(
                element_local_path,
                get_raw_data(element_url).content,
                content_tag,
            )
            replace_source_link(
                element,
                target_directory_path,
                name,
                content_tag,
            )
            bar.next()
            log_pars.info('The item is downloaded.')
        bar.finish()
    html_file_path = get_path(saving_url, local_path, 'html_page')
    with open(html_file_path, 'w') as write_file:
        write_file.write(page_html_tree.prettify())
    return html_file_path
