import os
import tempfile
import pytest
import requests_mock
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from .fixtures.for_fixtures import get_path_fixture, FAKE_LINKS
from page_loader.page_output import download
from unittest.mock import patch
from bs4 import BeautifulSoup as bs


url = FAKE_LINKS['normal_url']
dir_name = FAKE_LINKS['dir_for_resources']
html_name_hexlet = FAKE_LINKS['new_html_name']
png_source = 'https://ru.hexlet.io/assets/professions/nodejs.png'
fixt1 = get_path_fixture('one_png.html')
fixt2 = get_path_fixture('just_file.txt')
fixt3 = get_path_fixture('one_png_after.html')
new_png_path = "ru-hexlet-io-courses_files/" \
               "ru-hexlet-io-assets-professions-nodejs.png"
old_source = '/assets/professions/nodejs.png'



@pytest.mark.parametrize('code, new_source', [(200, new_png_path),
                                              (404, old_source)])

def test_download1(code, new_source):
    with tempfile.TemporaryDirectory() as t:
        page_path = os.path.join(t, html_name_hexlet)
        with requests_mock.Mocker() as m:
            m.get(url, text=open(fixt1, 'r').read(), status_code=200)
            m.get(png_source, text=open(fixt2, 'r').read(), status_code=code)
            assert page_path == download(url, t)
            with open(page_path, 'r') as f:
                soup = bs(f.read(), features="html.parser")
                test_res = soup.find_all('img')
                assert test_res[0]['src'] == new_source


@pytest.mark.parametrize('wrong_url', [FAKE_LINKS['invalid_url1'],
                                       FAKE_LINKS['invalid_url3'],
                                       html_name_hexlet])
def test_download2(wrong_url):
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises(CommonPageLoaderException):
            download(wrong_url, d)


def test_download3():
    with tempfile.TemporaryDirectory() as t:
        with requests_mock.Mocker() as m:
            m.get(url, text=open(fixt1, 'r').read(), status_code=500)
            with pytest.raises(CommonPageLoaderException):
                download(url, t)


@patch('page_loader.page_output.prepare_dir')
def test_download4(pd_mock):
    with tempfile.TemporaryDirectory() as t:
        pd_mock.side_effect = FileExistsError
        with requests_mock.Mocker() as m:
            m.get(url, text=open(fixt2, 'r').read(), status_code=200)
            with pytest.raises(FileExistsError):
                download(url, t)
