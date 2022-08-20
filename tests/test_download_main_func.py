import os
import tempfile
import pytest
import requests_mock
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from .fixtures.for_fixtures import get_path_fixture, FAKE_LINKS
from page_loader.page_output import download
from unittest.mock import patch


url = FAKE_LINKS['normal_url']
dir_name = FAKE_LINKS['dir_for_resources']
html_name_hexlet = FAKE_LINKS['new_html_name']
png_source = 'https://ru.hexlet.io/assets/professions/nodejs.png'
fixt1 = get_path_fixture('one_png.html')
fixt2 = get_path_fixture('just_file.txt')


@patch('page_loader.page_output.get_resources')
@patch('page_loader.page_output.user_friendly_message')
def test_download1(uf_mock, gr_mock):
    with tempfile.TemporaryDirectory() as t:
        page_path = os.path.join(t, html_name_hexlet)
        dir_path = os.path.join(t, dir_name)
        with requests_mock.Mocker() as m:
            m.get(url, text=open(fixt1, 'r').read(), status_code=200)
            m.get(png_source, text=open(fixt2, 'r').read(), status_code=404)
            assert page_path == download(url, t)
            gr_mock.assert_called_once_with(page_path, url, dir_name)
            uf_mock.assert_called_once_with('resource dir', dir_path)


@patch('page_loader.page_output.user_friendly_message')
def test_download2(uf_mock):
    with tempfile.TemporaryDirectory() as t:
        with requests_mock.Mocker() as m:
            m.get(url, text=open(fixt1, 'r').read(), status_code=500)
            with pytest.raises(CommonPageLoaderException):
                download(url, t)
            assert uf_mock.call_count


@patch('page_loader.page_output.prepare_dir')
def test_download3(pd_mock):
    with tempfile.TemporaryDirectory() as t:
        pd_mock.side_effect = FileExistsError
        with requests_mock.Mocker() as m:
            m.get(url, text=open(fixt2, 'r').read(), status_code=200)
            with pytest.raises(FileExistsError):
                download(url, t)
