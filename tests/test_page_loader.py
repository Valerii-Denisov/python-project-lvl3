import pytest
from page_loader import page_download
from page_loader.page_downloads import get_name
import requests_mock


URL = 'https://ru.hexlet.io/courses'
IMAGE_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
UNMODIFIED_FILE = '/home/valerii/python-project-lvl3/tests/fixtures/mocks/web_page.html'
HTML_FILE_NAME = 'ru-hexlet-io-courses.html'
MOCKING_IMAGE = '/home/valerii/python-project-lvl3/tests/fixtures/mocks/nodejs.png'
MODIFIED_FILE = '/home/valerii/python-project-lvl3/tests/fixtures/web_page_mod.html'


def read_file(file_path, teg='r'):
    with open(file_path, teg) as file:
        file_text = file.read()
    return file_text


def test_get_name():
    correct_name = HTML_FILE_NAME
    file_name = get_name(URL, 'html_page')
    assert file_name == correct_name


def test_page_download(tmp_path):
    with requests_mock.Mocker() as m:
        m.get(URL, text=read_file(UNMODIFIED_FILE))
        m.get(IMAGE_URL, content=read_file(MOCKING_IMAGE, 'rb'))
        path_file = page_download(URL, tmp_path)
        assert read_file(path_file) == read_file(MODIFIED_FILE)
