import os
import tempfile
import pytest
import requests_mock
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from .fixtures.for_fixtures import get_path_fixture, FAKE_LINKS
from page_loader.page_output import download, download_page, \
    get_resources
from unittest.mock import patch
from bs4 import BeautifulSoup as bs


URL = FAKE_LINKS['normal_url']
DIR_NAME = FAKE_LINKS['dir_for_resources']
HTML_NAME_HEXLET = FAKE_LINKS['new_html_name']
PNG_SOURCE = 'https://ru.hexlet.io/assets/professions/nodejs.png'
NEW_PNG_PATH = "ru-hexlet-io-courses_files/" \
               "ru-hexlet-io-assets-professions-nodejs.png"
OLD_SOURCE = "/assets/professions/nodejs.png"

FIXT1 = get_path_fixture('one_png.html')
FIXT2 = get_path_fixture('just_file.txt')
FIXT3 = get_path_fixture('one_png_after.html')


@patch('page_loader.page_output.request_http')
def test_download_page1(rh_mock):
    rh_mock.return_value = b'hello'
    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, HTML_NAME_HEXLET)
        download_page(path_file, URL)
        assert os.path.exists(path_file)
        with open(path_file, 'rb') as f:
            assert f.read() == b'hello'


def test_get_resources():
    fixt = get_path_fixture('before.html')
    with open(fixt, 'r', encoding='utf-8') as f:
        soup = bs(f.read(), features="html.parser")
        all_resources = get_resources(soup, URL)
        assert len(all_resources) == 5


@pytest.mark.parametrize('code, new_source', [(200, NEW_PNG_PATH),
                                              (404, OLD_SOURCE)])
def test_download1(code, new_source):
    with tempfile.TemporaryDirectory() as t:
        page_path = os.path.join(t, HTML_NAME_HEXLET)
        with requests_mock.Mocker() as m:
            m.get(URL, text=open(FIXT1, 'r').read(), status_code=200)
            m.get(PNG_SOURCE, text=open(FIXT2, 'r').read(), status_code=code)
            assert page_path == download(URL, t)
            with open(page_path, 'r') as f:
                soup = bs(f.read(), features="html.parser")
                test_res = soup.find_all('img')
                assert test_res[0]['src'] == new_source


@pytest.mark.parametrize('wrong_url', [FAKE_LINKS['invalid_url1'],
                                       FAKE_LINKS['invalid_url3'],
                                       HTML_NAME_HEXLET])
def test_download2(wrong_url):
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises(CommonPageLoaderException):
            download(wrong_url, d)


def test_download3():
    with tempfile.TemporaryDirectory() as t:
        with requests_mock.Mocker() as m:
            m.get(URL, text=open(FIXT1, 'r').read(), status_code=500)
            with pytest.raises(CommonPageLoaderException):
                download(URL, t)


@patch('page_loader.page_output.prepare_dir')
def test_download4(pd_mock):
    with tempfile.TemporaryDirectory() as t:
        pd_mock.side_effect = FileExistsError
        with requests_mock.Mocker() as m:
            m.get(URL, text=open(FIXT2, 'r').read(), status_code=200)
            with pytest.raises(FileExistsError):
                download(URL, t)


def test_download5():
    with requests_mock.Mocker() as m:
        m.get(URL, text=open(FIXT2, 'r').read(), status_code=200)
        with pytest.raises(CommonPageLoaderException):
            download(URL, 'SOME/DIRECTORY')
