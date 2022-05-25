import os
import requests_mock
import tempfile
from page_loader.page_output import download
from page_loader.page_parser import get_resources


def test_download():
    url = 'https://ru.hexlet.io/courses'
    html_name = 'ru-hexlet-io-courses.html'
    dir_name = 'ru-hexlet-io-courses_files'
    fixt = '/home/ulitka/python-project-lvl3/page_loader/tests/fixtures/before1.html'
    with requests_mock.Mocker() as m:
        m.get(url, text=open(fixt, 'r').read())
        with tempfile.TemporaryDirectory() as temp:
            new_page = download(url, output_path=temp)
            assert os.path.join(temp, html_name) == new_page
            assert os.path.exists(os.path.join(temp, dir_name))
            assert os.path.exists(new_page)


def test_get_resources():
    url = 'https://ru.hexlet.io/courses'
    html_name = 'ru-hexlet-io-courses.html'
    dir_name = 'ru-hexlet-io-courses_files'
    fixt = '/home/ulitka/python-project-lvl3/page_loader/tests/fixtures/before1.html'
    with tempfile.TemporaryDirectory() as temp:
        a = get_resources(fixt, url, temp)
    assert a == 7


