import requests
import re
import os

NAME_PATTERN = r'(?<=//).+'


def page_download(address, local_path):
    page = requests.get(address)
    dir_path = os.path.join(local_path, get_name(address) + '_files')
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, get_name(address) + '.html')
    with open(file_path, 'a') as file:
        file.write(page.text)
    return file_path


def get_name(raw_address):
    raw_name = re.search(NAME_PATTERN, raw_address)
    return re.sub(r'(\/|\.)', '-', raw_name.group())
