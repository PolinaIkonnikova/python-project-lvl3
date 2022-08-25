import os
import tempfile
import pytest
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from .fixtures.for_fixtures import FAKE_LINKS
from page_loader.files_and_dirs import make_name, valid_dir,\
    prepare_dir


URL = FAKE_LINKS['normal_url']
DIR_NAME = FAKE_LINKS['dir_for_resources']
HTML_NAME_HEXLET = FAKE_LINKS['new_html_name']


@pytest.mark.parametrize('file_name, output_name',
                         [(URL, HTML_NAME_HEXLET),
                          ('/assets/professions/nodejs.png',
                           'assets-professions-nodejs.png'),
                          ('/ru.hexlet.io/courses.html',
                           'ru-hexlet-io-courses.html')])
def test_make_name(file_name, output_name):
    assert make_name(file_name) == output_name


def test_make_dir_name():
    assert make_name(URL, is_dir=True) == DIR_NAME


@pytest.mark.parametrize('path', [FAKE_LINKS['invalid_url3'],
                                  'some_dir.png', URL])
def test_valid_dir(path):
    with pytest.raises(CommonPageLoaderException):
        valid_dir(path)


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
