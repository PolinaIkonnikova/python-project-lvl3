import os
import tempfile
import pytest
import shutil
import requests_mock
from bs4 import BeautifulSoup as bs
from page_loader.resources_output import download_resources, get_resources
from .fixtures.for_fixtures import FAKE_LINKS,\
    get_path_fixture
from page_loader.work_with_files import prepare_dir


URL = FAKE_LINKS['normal_url']
DIR_NAME = FAKE_LINKS['dir_for_resources']
HTML_NAME_HEXLET = FAKE_LINKS['new_html_name']
NEW_PNG_PATH = "ru-hexlet-io-courses_files/" \
               "ru-hexlet-io-assets-professions-nodejs.png"
NEW_PNG_SOURCE = 'https://ru.hexlet.io/assets/professions/nodejs.png'


def test_prepare_dir1():
    with tempfile.TemporaryDirectory() as t:
        dir_name, dir_path = prepare_dir(URL, t)
        assert os.path.exists(dir_path)
        assert dir_name == DIR_NAME


def test_prepare_dir2():
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises(FileExistsError):
            os.mkdir(os.path.join(d, DIR_NAME))
            prepare_dir(URL, d)


def test_get_resources():
    fixt = get_path_fixture('before.html')
    with open(fixt, 'r', encoding='utf-8') as f:
        soup = bs(f.read(), features="html.parser")
        all_resources = get_resources(soup, URL)
        assert len(all_resources) == 5


def test_download_resources():
    fixt1 = get_path_fixture('one_png.html')
    fixt2 = get_path_fixture('just_file.txt')
    with tempfile.TemporaryDirectory() as t:
        os.mkdir(os.path.join(t, 'ru-hexlet-io-courses_files'))
        temp_fixt = shutil.copyfile(fixt1, os.path.join(t, 'test.html'))
        with requests_mock.Mocker() as m:
            m.get(NEW_PNG_SOURCE, text=open(fixt2, 'r').read(),
                  status_code=200)
            download_resources(temp_fixt, URL, DIR_NAME, t)

        with open(temp_fixt, 'r') as f:
            soup = bs(f.read(), features="html.parser")
            test_res = soup.find_all('img')
            assert test_res[0]['src'] == NEW_PNG_PATH

        assert os.path.exists(os.path.join(t, NEW_PNG_PATH))


def test_download_resources2():
    fixt = get_path_fixture('empty.html')
    with tempfile.TemporaryDirectory() as t:
        assert download_resources(fixt, URL, DIR_NAME, t) is None
