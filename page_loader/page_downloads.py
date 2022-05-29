import requests
import re
import os
from bs4 import BeautifulSoup
import urllib.request as urllib


def page_download(address, local_path):
    page = requests.get(address)
    dir_path = os.path.join(local_path, get_name(address) + '_files')
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, get_name(address) + '.html')
    text = page.text
    for element in find_some(page.text, 'img'):
        if re.search(r'png|jpg', element['src']):
            element_address = re.sub(r'([a-z]*:*)//|^/', 'http://', element['src'])
            print(element_address)
            element_name = re.search(r'[a-zA-Z0-9-]*(?=-jpg|-png)', get_name(element_address))
            element_file_path = os.path.join(dir_path, element_name.group() + '.png')
            print(element_file_path)
            urllib.urlretrieve(element_address, element_file_path)
            text = re.sub(element['src'], element_file_path, text)
    with open(file_path, 'a') as file:
        file.write(text)
    return file_path


def get_name(raw_address):
    raw_name = re.search(r'(?<=//).+', raw_address)
    return re.sub(r'(\/|\.)', '-', raw_name.group())


def find_some(html_file, tag):
    soup = BeautifulSoup(html_file, 'html.parser')
    return soup.find_all(tag)
       
    