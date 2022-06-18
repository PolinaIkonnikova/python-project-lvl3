import os
import requests_mock
import tempfile
import shutil
import pytest
from page_loader.page_output import download, get_resources, writing_page, download_source, make_dir


#@pytest.mark.skip
@pytest.fixture
def test_make_new_dir(normal_url_hexlet, some_string, dir_name_hexlet):
    url = normal_url_hexlet
    dir_name = dir_name_hexlet
    fake_path = some_string

    with tempfile.TemporaryDirectory() as temp:
        make_dir(url, temp)
        assert(os.path.exists(os.path.join(temp, dir_name)))

    try:
        make_dir(url, fake_path)
    except SystemExit:
        assert 1


#@pytest.mark.skip
@pytest.fixture
def test_download_page(fake_resources, normal_url_hexlet, html_name_hexlet):
    url = normal_url_hexlet
    html_name = html_name_hexlet
    fixt = '/home/ulitka/python-project-lvl3/page_loader/tests/fixtures/before1.html'
    with requests_mock.Mocker() as m:
        m.get(url, text=open(fixt, 'r').read())
        with tempfile.TemporaryDirectory() as temp:
            new_page = download(url, output_path=temp, downloading_res=fake_resources)
            assert os.path.join(temp, html_name) == new_page
            assert os.path.exists(new_page)


#@pytest.mark.skip
@pytest.fixture
def test_writing_page(some_string):

    fake_url = 'htps:/' + some_string
    try:
        writing_page(fake_url, 'some_path')
    except SystemExit:
        assert 1


@pytest.fixture
def test_download_source(normal_img, fake_img):
    with tempfile.TemporaryDirectory() as temp:
        image_for_test = os.path.join(temp, '1.jpg')
        try:
            download_source(image_for_test, normal_img)
            download_source(image_for_test, fake_img)
        except SystemExit:
            assert 0


#@pytest.mark.skip
@pytest.fixture
def test_get_resources(fake_downloading, normal_url_hexlet):
    url = normal_url_hexlet
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
