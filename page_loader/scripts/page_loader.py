#!/usr/bin/env python
"""The main script of the project."""

import argparse as ap
import os
import sys

import requests
from page_loader import download


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
    try:
        path = download(args.address, args.output)
    except requests.exceptions.HTTPError:
        print('Page cannot be loaded. Find HTTP error.')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print('A Connection error occurred.')
        sys.exit(1)
    except requests.exceptions.Timeout:
        print('The request timed out.')
        sys.exit(1)
    except PermissionError:
        print('Cannot write to directory, check permission for directory.')
        sys.exit(1)
    except FileNotFoundError:
        print('Target directory not found, check path to directory.')
        sys.exit(1)
    else:
        print('Downloading complete! Path to file: {0}'.format(path))
        sys.exit(0)


if __name__ == '__main__':
    main()
