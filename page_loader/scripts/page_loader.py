#!/usr/bin/env python
"""The main script of the project."""

import argparse as ap
import logging.config
import os
import sys

import requests
from page_loader import page_download
from page_loader.logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger('app_logger')


def main():
    """Display info of package."""
    parser = ap.ArgumentParser(description='Page-loader')
    parser.add_argument(
        '-o',
        '--output',
        default=os.getcwd(),
        help='Directory to save',
    )
    parser.add_argument('address')
    args = parser.parse_args()
    try:
        log.info('Start downloading page: {0}'.format(args.address))
        path = page_download(args.address, args.output)
        log.info('Downloading complete! Path to file: {0}'.format(path))
        sys.exit(0)
    except requests.exceptions.ConnectionError as error:
        log.critical(error)


if __name__ == '__main__':
    main()
