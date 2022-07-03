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
    print('Start downloading page: {0}'.format(args.address))
    try:
        path = download(args.address, args.output)
    except requests.exceptions.RequestException:
        sys.exit(1)
    except PermissionError:
        sys.exit(1)
    except FileNotFoundError:
        sys.exit(1)
    else:
        print('Downloading complete! Path to file: {0}'.format(path))
        sys.exit(0)


if __name__ == '__main__':
    main()
