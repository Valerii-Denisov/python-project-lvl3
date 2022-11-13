import pytest
from page_loader import download
from page_loader.naming import get_file_name
import os
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
MODIFIED_FILE_WITH_ERROR = 'tests/fixtures/web_page_mod_error.html'
WRONG_FILE_PATH = '/home/valerii/some_folder'
WRONG_RULE_FILE_PATH = '/home'
TARGET_IMAGE_FILE = 'ru-hexlet-io-assets-professions-nodejs.png'
TARGET_JS_FILE = 'ru-hexlet-io-packs-js-runtime.js'
TARGET_CSS_FILE = 'ru-hexlet-io-assets-application.css'
TARGET_FOLDER = 'ru-hexlet-io-courses_files'
CODE = {404, 403, 500}
ERRORS = {
    requests.exceptions.Timeout,
    requests.exceptions.RequestException,
    requests.exceptions.HTTPError,
    requests.exceptions.ConnectionError,
}


def read_file(file_path, teg='r'):
    with open(file_path, teg) as file:
        file_text = file.read()
    return file_text


def test_get_name():
    correct_name = HTML_FILE_NAME
    file_name = get_file_name(URL)
    assert file_name == correct_name


def test_page_download(requests_mock, tmp_path):
    requests_mock.get(URL, text=read_file(UNMODIFIED_FILE))
    requests_mock.get(IMAGE_URL, content=read_file(MOCKING_IMAGE, 'rb'))
    requests_mock.get(JS_URL, content=read_file(MOCKING_JS_FILE, 'rb'))
    requests_mock.get(CSS_URL, content=read_file(MOCKING_CSS_FILE, 'rb'))
    path_file = download(URL, tmp_path)
    image_path = os.path.join(tmp_path, TARGET_FOLDER, TARGET_IMAGE_FILE)
    css_path = os.path.join(tmp_path, TARGET_FOLDER, TARGET_CSS_FILE)
    js_path = os.path.join(tmp_path, TARGET_FOLDER, TARGET_JS_FILE)
    inner_html_path = os.path.join(tmp_path, TARGET_FOLDER, HTML_FILE_NAME)
    assert read_file(path_file) == read_file(MODIFIED_FILE)
    assert read_file(image_path, 'rb') == read_file(MOCKING_IMAGE, 'rb')
    assert read_file(css_path, 'rb') == read_file(MOCKING_CSS_FILE, 'rb')
    assert read_file(js_path, 'rb') == read_file(MOCKING_JS_FILE, 'rb')
    assert read_file(inner_html_path, 'rb') == read_file(UNMODIFIED_FILE, 'rb')


def test_page_download_with_error(requests_mock, tmp_path):
    requests_mock.get(URL, text=read_file(UNMODIFIED_FILE))
    requests_mock.get(IMAGE_URL, status_code=404)
    requests_mock.get(JS_URL, content=read_file(MOCKING_JS_FILE, 'rb'))
    requests_mock.get(CSS_URL, content=read_file(MOCKING_CSS_FILE, 'rb'))
    path_file = download(URL, tmp_path)
    assert read_file(path_file) == read_file(MODIFIED_FILE_WITH_ERROR)


@pytest.mark.parametrize('error_code', CODE)
def test_response_with_error(error_code, tmp_path, requests_mock):
    requests_mock.get(URL, status_code=error_code)
    with pytest.raises(Exception):
        assert download(URL, tmp_path)


@pytest.mark.parametrize('error', ERRORS)
def test_for_http_error(error, tmp_path, requests_mock):
    requests_mock.get(URL, exc=error)
    with pytest.raises(error):
        assert not download(URL, tmp_path)


@pytest.mark.parametrize(
    'error, filepath',
    [(FileNotFoundError, WRONG_FILE_PATH),
     (PermissionError, WRONG_RULE_FILE_PATH),
     ],
)
def test_download_with_local_error(requests_mock, error, filepath):
    requests_mock.get(URL)
    with pytest.raises(error):
        assert not download(URL, filepath)
