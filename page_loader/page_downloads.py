
import os
import re
import types
import urllib.parse as parser

import requests
from bs4 import BeautifulSoup

SUFFIX = types.MappingProxyType({
    'directory': '_files',
    'html_page': '.html',
    'images': '.png',
})
CONTENT_TYPE = types.MappingProxyType({
    'images': dict(tag='img', pattern=r'png|jpg', linc='src', write='wb'),
})


def page_download(url, local_path):
    directory_path = get_path(url, local_path, 'directory')
    make_directory(directory_path)
    page_content = requests.get(url).text
    page_content = save_content(
        page_content,
        parser.urlparse(url).netloc,
        directory_path,
        'images',
    )
    html_file_path = get_path(url, local_path, 'html_page')
    with open(html_file_path, 'w') as write_file:
        write_file.write(page_content)
    return html_file_path


def get_name(raw_address, object_type, home_netloc=''):
    url_data = parser.urlparse(raw_address)
    raw_name = '{0}{1}{2}'.format(home_netloc, url_data.netloc, url_data.path)
    name = re.sub(r'(/|[.])', '-', raw_name)
    if object_type == 'images':
        element_name = re.search(
            r"[a-zA-Z\d-]*(?=-jpg|-png)",
            name,
        )
        return element_name.group() + SUFFIX[object_type]
    return name + SUFFIX[object_type]


def find_some(html_file, tag):
    soup = BeautifulSoup(html_file, 'html.parser')
    return soup.find_all(tag)


def make_directory(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def get_path(url, local_path, source_type):
    return os.path.join(local_path, get_name(url, source_type))


def save_content(content, home_netloc, directory, resource_type):
    for element in find_some(content, CONTENT_TYPE[resource_type]['tag']):
        if re.search(
            CONTENT_TYPE[resource_type]['pattern'],
            element[CONTENT_TYPE[resource_type]['linc']],
        ):
            object_url_data = parser.urlparse(
                element[CONTENT_TYPE[resource_type]['linc']],
            )
            if object_url_data.netloc in {'', home_netloc}:
                element_local_path = '{0}/{1}'.format(
                    directory,
                    get_name(
                        element[CONTENT_TYPE[resource_type]['linc']],
                        resource_type,
                        home_netloc,
                    ),
                )
                element_url = 'https://{0}{1}'.format(
                    home_netloc,
                    object_url_data.path,
                )
                with open(
                    element_local_path,
                    CONTENT_TYPE[resource_type]['write'],
                ) as write_file:
                    write_file.write(requests.get(element_url).content)
                return re.sub(
                    element[CONTENT_TYPE[resource_type]['linc']],
                    element_local_path,
                    content,
                )
