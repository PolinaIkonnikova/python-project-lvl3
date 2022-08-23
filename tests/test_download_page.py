import os
import tempfile
import pytest
from unittest.mock import patch
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from .fixtures.for_fixtures import get_path_fixture, FAKE_LINKS
from page_loader.page_output import download_page
from page_loader.work_with_files import make_name, valid_dir, write_file
from page_loader.aux.print_message import user_friendly_message

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
    assert make_name(file_name) == output_name


def test_true_dir_naming():
    assert make_name(url, is_dir=True) == dir_name


@pytest.mark.parametrize('path', [FAKE_LINKS['invalid_url3'],
                                  'some_dir.png', url])
def test_valid_dir(path):
    with pytest.raises(CommonPageLoaderException):
        valid_dir(path)


def test_writing_text():
    data = 'hello'
    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, 'new_file.html')
        write_file(path_file, data)
        with open(path_file, 'r') as f:
            assert data == f.read()


def test_writing_bytes():
    fixt = get_path_fixture('meow.jpeg')
    pic_size = os.path.getsize(fixt)
    with open(fixt, 'rb') as f:
        data = f.read()

    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, 'meow2.jpeg')
        write_file(path_file, data, bytes=True)
        pic_size2 = os.path.getsize(path_file)
        assert pic_size == pic_size2


@patch('page_loader.page_output.request_http')
def test_download_page1(rh_mock):
    rh_mock.return_value = 'hello'
    with tempfile.TemporaryDirectory() as d:
        path_file = os.path.join(d, html_name_hexlet)
        new_html = download_page(url, d)
        assert os.path.exists(new_html)
        assert new_html == path_file


@pytest.mark.parametrize('wrong_url', [FAKE_LINKS['invalid_url1'],
                                       FAKE_LINKS['invalid_url3'],
                                       html_name_hexlet])
def test_download_page2(wrong_url):
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises(CommonPageLoaderException):
            download_page(wrong_url, d)


r1 = 'The page not found, sorry.\n'
r2 = 'There is a browser error, try again later!\n'
r3 = "The directory not found or not " \
     "a directory, please try again!\n"
r4 = "The directory for resources: "


@pytest.mark.parametrize('message, response', [('not found dir', r3),
                                               ('404', r1),
                                               ('402', r2)])
def test_user_friendly_message1(capsys, message, response):
    user_friendly_message(message)
    out, err = capsys.readouterr()
    assert out == response


def test_user_friendly_message2(capsys):
    user_friendly_message('resource dir', dir_name)
    out, err = capsys.readouterr()
    assert out == r4 + dir_name + "\n"
