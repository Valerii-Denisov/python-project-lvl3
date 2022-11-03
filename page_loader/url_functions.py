"""The module contains the main functions for working with url."""

import logging
from urllib import parse as parser

log_pars = logging.getLogger('app_logger')


def get_source_url(parsing_url, element, link):
    """
    Build the url of the element.

    Parameters:
        element: tag;
        parsing_url: string;
        link: string.

    Returns:
          URL-address.
    """
    object_url_data = parser.urlparse(
        element[link],
    )
    return '{2}://{0}{1}'.format(
        parsing_url.netloc,
        object_url_data.path,
        parsing_url.scheme,
    )


def get_url_with_netloc(raw_address, home_netloc):
    """
    Build full url.

    Parameters:
        raw_address: string;
        home_netloc: string.

    Returns:
          File name.
    """
    url_data = parser.urlparse(raw_address)
    if url_data.netloc:
        raw_url = '{0}{1}'.format(url_data.netloc, url_data.path)
    else:
        raw_url = '{0}{1}'.format(home_netloc, url_data.path)
    return raw_url
