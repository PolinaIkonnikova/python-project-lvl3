import os
import tempfile
import pytest
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from page_loader.tests.fixtures.for_fixtures import get_path_fixture, FAKE_LINKS
from page_loader.page_output import download_page
from page_loader.work_with_files import true_name, valid_dir, writing


url = FAKE_LINKS['normal_url']
dir_name = FAKE_LINKS['dir_for_resources']
html_name_hexlet = FAKE_LINKS['new_html_name']


@pytest.mark.parametrize('file_name, output_name',
                         [(url, html_name_hexlet),
                          ('/assets/professions/nodejs.png',
                           'assets-professions-nodejs.png'),
                          ('/ru.hexlet.io/courses.html',
                           'ru-hexlet-io-courses.html')])
def test_true_naming(file_name, output_name):
    assert true_name(file_name) == output_name


def test_true_dir_naming():
    assert true_name(url, is_dir=True) == dir_name


@pytest.mark.parametrize('path', [FAKE_LINKS['invalid_url3'],
                                  'some_dir.png', url])
def test_valid_dir(path):
    with pytest.raises(CommonPageLoaderException):
        valid_dir(path)


def test_writing_text():
    data = 'hello'
    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, 'new_file.html')
        writing(path_file, data)
        with open(path_file, 'r') as f:
            assert data == f.read()


def test_writing_bytes():
    fixt = get_path_fixture('meow.jpeg')
    pic_size = os.path.getsize(fixt)
    with open(fixt, 'rb') as f:
        data = f.read()

    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, 'meow2.jpeg')
        writing(path_file, data, bytes=True)
        pic_size2 = os.path.getsize(path_file)
        assert pic_size == pic_size2


def fake_data(*args):
    return 'hello'


def test_download_page1():
    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, html_name_hexlet)
        new_html = download_page(url, d, get_content=fake_data)
        assert os.path.exists(new_html)
        assert new_html == path_file


@pytest.mark.parametrize('wrong_url', [FAKE_LINKS['invalid_url1'],
                                       FAKE_LINKS['invalid_url3'],
                                       html_name_hexlet])
def test_download_page2(wrong_url):
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises(CommonPageLoaderException):
            download_page(wrong_url, d)
