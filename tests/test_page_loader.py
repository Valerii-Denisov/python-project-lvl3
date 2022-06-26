import os.path

import pytest
from page_loader import download
from page_loader.naming_functions import get_name
from page_loader.url_functions import get_raw_data
from page_loader.file_functions import make_directory
import requests_mock
import requests


URL = 'https://ru.hexlet.io/courses'
IMAGE_URL = 'https://ru.hexlet.io/assets/professions/nodejs.png'
JS_URL = 'https://ru.hexlet.io/packs/js/runtime.js'
CSS_URL = 'https://ru.hexlet.io/assets/application.css'
UNMODIFIED_FILE = 'tests/fixtures/mocks/web_page.html'
HTML_FILE_NAME = 'ru-hexlet-io-courses.html'
MOCKING_IMAGE = 'tests/fixtures/mocks/nodejs.png'
MOCKING_JS_FILE = 'tests/fixtures/mocks/js_file.js'
MOCKING_CSS_FILE = 'tests/fixtures/mocks/css_file.css'
MODIFIED_FILE = 'tests/fixtures/web_page_mod.html'
CODE = {404, 403, 500}
ERRORS = {
    requests.exceptions.HTTPError,
    requests.exceptions.Timeout,
    requests.exceptions.RequestException,
}


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
        m.get(JS_URL, content=read_file(MOCKING_JS_FILE, 'rb'))
        m.get(CSS_URL, content=read_file(MOCKING_CSS_FILE, 'rb'))
        path_file = download(URL, tmp_path)
        assert read_file(path_file) == read_file(MODIFIED_FILE)


@pytest.mark.parametrize('error_code', CODE)
def test_get_raw_data(error_code):
    with requests_mock.Mocker() as m:
        m.get(URL, text=read_file(UNMODIFIED_FILE), status_code=error_code)
        with pytest.raises(requests.exceptions.HTTPError):
            assert get_raw_data(URL)


def test_permission_error():
    with requests_mock.Mocker() as m:
        m.get(URL, text=read_file(UNMODIFIED_FILE))
        filepath = '/some_filepath'
        with pytest.raises(PermissionError):
            assert make_directory(filepath)


def test_file_not_found_error():
    with requests_mock.Mocker() as m:
        m.get(URL, text=read_file(UNMODIFIED_FILE))
        filepath = './home/valerii/wrong_directory'
        with pytest.raises(FileNotFoundError):
            assert make_directory(filepath)
