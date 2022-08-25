import os
import tempfile
import pytest
from bs4 import BeautifulSoup as bs
from .fixtures.for_fixtures import FAKE_LINKS,\
    get_path_fixture
from page_loader.work_with_files import prepare_dir
from page_loader.page_output import get_resources

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
