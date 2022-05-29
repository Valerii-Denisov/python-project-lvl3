import pytest
from page_loader import page_download
from page_loader.page_downloads import get_name


URL = 'https://ru.hexlet.io/courses'
HTML_FILE_NAME = 'ru-hexlet-io-courses'
DIRECTORY = '/home/valerii/proba'

def test_get_name():
    correct_name = HTML_FILE_NAME
    file_name = get_name(URL)
    assert file_name == correct_name

