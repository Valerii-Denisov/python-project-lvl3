#!/usr/bin/env python
"""The main script of the project."""

import argparse as ap
import os

import requests
from page_loader import page_download


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
        print(page_download(args.address, args.output))
    except requests.exceptions.ConnectionError:
        print('ops')


if __name__ == '__main__':
    main()
