#!/usr/bin/env python
"""The main script of the project."""

import argparse as ap
import logging.config
import os
import sys

import requests
from page_loader import download
from page_loader.logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger('app_logger')
file_log = logging.getLogger('file_logger')


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
    print('Trying to downloading page: {0}'.format(args.address))
    file_log.info('Trying to downloading page: {0}'.format(args.address))
    try:
        path = download(args.address, args.output)
    except requests.exceptions.HTTPError:
        log.critical('Page cannot be loaded. Find HTTP error.')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        log.critical('A Connection error occurred.')
        sys.exit(1)
    except requests.exceptions.Timeout:
        log.critical('The request timed out.')
        sys.exit(1)
    except PermissionError:
        log.error(
            'Cannot write to directory, check permission for directory.',
        )
        sys.exit(1)
    except FileNotFoundError:
        log.error(
            'Target directory not found, check path to directory.',
        )
        sys.exit(1)
    else:
        print('Downloading complete! Path to file: {0}'.format(path))
        file_log.info('Downloading complete! Path to file: {0}'.format(path))
        sys.exit(0)


if __name__ == '__main__':
    main()
