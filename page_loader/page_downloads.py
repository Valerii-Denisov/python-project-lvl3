import requests
import re
import os


def page_download(address, local_path):
    page = requests.get(address)
    re_pattern = r'(?<=//).+'
    raw_name = re.search(re_pattern, address)
    file_name = re.sub(r'(\/|\.)', '-', raw_name.group()) + '.html'
    file_path = os.path.join(local_path, file_name)
    text = page.text
    with open(file_path, 'a') as file:
        file.write(text)
    return file_path
