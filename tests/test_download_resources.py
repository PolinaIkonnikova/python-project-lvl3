import os
import tempfile
import pytest
import shutil
from bs4 import BeautifulSoup as bs
from page_loader.resources_output import get_resources, download_resources
from tests.fixtures.stubs_and_fixt import fake_writing, FAKE_LINKS, get_abs_path_fixture
from page_loader.work_with_files import prepare_dir
from page_loader.aux.custom_exceptions import NoResourcesException


url = FAKE_LINKS['normal_url']
dir_name = FAKE_LINKS['dir_for_resources']
html_name_hexlet = FAKE_LINKS['new_html_name']
fixt1 = get_abs_path_fixture('one_png.html')
fixt2 = get_abs_path_fixture('before1.html')


def test_prepare_dir1():
    with tempfile.TemporaryDirectory() as d:
        dir_pass = prepare_dir(url, d)
        assert os.path.exists(os.path.join(d, dir_name))
        assert dir_pass == os.path.join(d, dir_name)


def test_prepare_dir2():
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises(FileExistsError):
            os.mkdir(os.path.join(d, dir_name))
            prepare_dir(url, d)


def test_download_resources1():
    res_dict1 = [{'tag': 'script',
                  'source': "https://ru.hexlet.io/packs/js/runtime.js",
                  'res_path': "ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js"},
                 {'source': "https://ru.hexlet.io/meow.png",
                  'tag': 'img',
                  'res_path': "meow.png"}]
    with tempfile.TemporaryDirectory() as temp:
        os.mkdir(os.path.join(temp, dir_name))
        download_resources(res_dict1, temp, writing_res=fake_writing)
        assert os.path.exists(os.path.join(temp, "meow.png"))
        assert os.path.exists(os.path.join(temp, "ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js"))


def test_download_resources2():
    res_dict = []
    with pytest.raises(NoResourcesException):
        download_resources(res_dict, 'some_dir', writing_res=fake_writing)


def test_get_resources1():
    new_png_path = "ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png"
    new_png_source = 'https://ru.hexlet.io/assets/professions/nodejs.png'
    with tempfile.TemporaryDirectory() as temp:
        temp_fixt = shutil.copyfile(fixt1, os.path.join(temp, 'test.html'))
        resources = get_resources(temp_fixt, url, dir_name)
        res = resources[0]

        assert res['tag'] == 'img'
        assert res['source'] == new_png_source
        assert res['res_path'] == new_png_path

        with open(temp_fixt, 'r') as f:
            soup = bs(f.read(), features="html.parser")
            test_res = soup.find_all('img')
            assert test_res[0]['src'] == new_png_path


def test_get_resources2():
    with tempfile.TemporaryDirectory() as temp:
        temp_fixt = shutil.copyfile(fixt2, os.path.join(temp, 'test.html'))
        resources = get_resources(temp_fixt, url, temp)
        assert len(resources) == 4
