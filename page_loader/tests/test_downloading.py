import os
import requests_mock
import tempfile
import pytest
import shutil
from page_loader.page_output import download, download_source, get_resources


# some_string = 'olololo.html'
# url_error_schema = ''
normal_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZmNcheLzMthy3Q04NhmZcdewmZG6vq1NjJg&usqp=CAU'
fake_image = 'htps://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZmNcheLzMthy3Q04NhmZcdewmZG6vq1NjJg&usqp=CAU'
# normal_url_hexlet = 'https://ru.hexlet.io/courses'
# dir_name_hexlet = 'ru-hexlet-io-courses_files'
# html_name_hexlet = 'ru-hexlet-io-courses.html'


@pytest.fixture
def fake_resources(*args):
    pass


@pytest.fixture
def fake_downloading(path, *args):
    with open(path, 'x'):
        pass

@pytest.mark.skip
def test_download_page(fake_resources):
    url = 'https://ru.hexlet.io/courses'
    html_name = 'ru-hexlet-io-courses.html'
    fixt = '/home/ulitka/python-project-lvl3/page_loader/tests/fixtures/before1.html'
    with requests_mock.Mocker() as m:
        m.get(url, text=open(fixt, 'r').read())
        with tempfile.TemporaryDirectory() as temp:
            new_page = download(url, output_path=temp, downloading_res=fake_resources)
            assert os.path.join(temp, html_name) == new_page
            assert os.path.exists(new_page)

@pytest.mark.skip
def test_download_source():
    #normal_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZmNcheLzMthy3Q04NhmZcdewmZG6vq1NjJg&usqp=CAU'
    fake_img = 'htps://encrypted-tbn0.gstatic.com/ololo'
    with tempfile.TemporaryDirectory() as temp:
        image_for_test = os.path.join(temp, '1.jpg')
        try:
            download_source(image_for_test, normal_img)
            download_source(image_for_test, fake_img)
        except SystemExit:
            assert 0


def test_get_resources(fake_downloading):
    url = 'https://ru.hexlet.io/courses'
    file_name1 = 'ru-hexlet-io-assets-application.css'
    file_name2 = 'ru-hexlet-io-packs-js-runtime.js'
    file_name3 = 'cdn2-hexlet-io-assets-menu.css'
    fixt = os.path.abspath(os.path.join('./page_loader/tests/fixtures', 'before1.html'))
    with tempfile.TemporaryDirectory() as temp:
        temp_fixt = shutil.copyfile(fixt, os.path.join(temp, 'before.html'))
        get_resources(temp_fixt, url, temp, downloading=fake_downloading)
        files = [f for f in os.listdir(temp) if os.path.isfile(os.path.join(temp, f))]
        assert len(files) == 5
        assert os.path.exists(os.path.join(temp, file_name1))
        assert os.path.exists(os.path.join(temp, file_name2))
        assert not os.path.exists(os.path.join(temp, file_name3))