import os
import tempfile
import pytest
import shutil
from bs4 import BeautifulSoup as bs
from page_loader.resources_output import get_resources,\
    download_resources
from tests.fixtures.for_fixtures import FAKE_LINKS,\
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


def fake_writing(res, output_path):
    path = os.path.join(output_path, res['res_path'])
    with open(path, 'x'):
        pass


def test_download_resources1():
    with tempfile.TemporaryDirectory() as t:
        res_path1 = os.path.join(t, "ru-hexlet-io-courses_files/"
                                    "ru-hexlet-io-packs-js-runtime.js")
        res_path2 = os.path.join(t, "meow.png")
        res_dict1 = [{'tag': 'script',
                      'source': "https://ru.hexlet.io/packs/js/runtime.js",
                      'res_path': res_path1},
                     {'source': "https://ru.hexlet.io/meow.png",
                      'tag': 'img',
                      'res_path': res_path2}]
        os.mkdir(os.path.join(t, DIR_NAME))
        download_resources(res_dict1, t, writing_res=fake_writing)
        assert os.path.exists(res_path1)
        assert os.path.exists(res_path2)


def test_download_resources2():
    res_dict = []
    assert download_resources(res_dict, 'some_dir') is None


def test_get_resources1():
    fixt = get_path_fixture('one_png.html')
    with tempfile.TemporaryDirectory() as t:
        temp_fixt = shutil.copyfile(fixt, os.path.join(t, 'test.html'))
        resources = get_resources(temp_fixt, URL, DIR_NAME)
        res = resources[0]
        assert res['tag'] == 'img'
        assert res['source'] == NEW_PNG_SOURCE
        assert res['res_path'] == NEW_PNG_PATH

        with open(temp_fixt, 'r') as f:
            soup = bs(f.read(), features="html.parser")
            test_res = soup.find_all('img')
            assert test_res[0]['src'] == NEW_PNG_PATH


def test_get_resources2():
    fixt = get_path_fixture('before.html')
    with tempfile.TemporaryDirectory() as t:
        temp_fixt = shutil.copyfile(fixt, os.path.join(t, 'test.html'))
        resources = get_resources(temp_fixt, URL, t)
        assert len(resources) == 4
