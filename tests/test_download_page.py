import os
import tempfile
import pytest
from unittest.mock import patch
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from .fixtures.for_fixtures import FAKE_LINKS
from page_loader.page_output import download_page
from page_loader.work_with_files import make_name, valid_dir


url = FAKE_LINKS['normal_url']
dir_name = FAKE_LINKS['dir_for_resources']
html_name_hexlet = FAKE_LINKS['new_html_name']


@pytest.mark.parametrize('file_name, output_name',
                         [(url, html_name_hexlet),
                          ('/assets/professions/nodejs.png',
                           'assets-professions-nodejs.png'),
                          ('/ru.hexlet.io/courses.html',
                           'ru-hexlet-io-courses.html')])
def test_make_name(file_name, output_name):
    assert make_name(file_name) == output_name


def test_make_dir_name():
    assert make_name(url, is_dir=True) == dir_name


@pytest.mark.parametrize('path', [FAKE_LINKS['invalid_url3'],
                                  'some_dir.png', url])
def test_valid_dir(path):
    with pytest.raises(CommonPageLoaderException):
        valid_dir(path)


@patch('page_loader.page_output.request_http')
def test_download_page1(rh_mock):
    rh_mock.return_value = b'hello'
    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, html_name_hexlet)
        download_page(path_file, url)
        assert os.path.exists(path_file)
        with open(path_file, 'rb') as f:
            assert f.read() == b'hello'

