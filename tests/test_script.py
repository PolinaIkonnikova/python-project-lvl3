import os
import requests_mock
import pytest
import tempfile
from page_loader.scripts.page_loader import main
from tests.fixtures.for_fixtures import FAKE_LINKS, get_path_fixture
from unittest.mock import patch

OK_URL = FAKE_LINKS['normal_url']


@patch('page_loader.scripts.page_loader.create_parser')
def test_script_page_loader_exit1(cp_mock):
    with tempfile.TemporaryDirectory() as t:
        png_source = 'https://ru.hexlet.io/assets/professions/nodejs.png'
        fixt1 = get_path_fixture('one_png.html')
        fixt2 = get_path_fixture('just_file.txt')
        cp_mock.return_value = OK_URL, t
        with requests_mock.Mocker() as m:
            m.get(OK_URL, text=open(fixt1, 'r').read(), status_code=200)
            m.get(png_source, text=open(fixt2, 'r').read(), status_code=404)
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 0


@patch('page_loader.scripts.page_loader.create_parser')
def test_script_page_loader_exit2(cp_mock):
    fixt = get_path_fixture('empty.html')
    with tempfile.TemporaryDirectory() as t:
        cp_mock.return_value = OK_URL, t
        with requests_mock.Mocker() as m:
            m.get(OK_URL, text=open(fixt, 'r').read(), status_code=500)
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 1


@pytest.mark.parametrize('warning_url', [FAKE_LINKS['invalid_url1'],
                                         FAKE_LINKS['invalid_url3'],
                                         FAKE_LINKS['invalid_url4']])
@patch('page_loader.scripts.page_loader.create_parser')
def test_script_page_loader_exit3(cp_mock, warning_url):
    with tempfile.TemporaryDirectory() as t:
        cp_mock.return_value = warning_url, t
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 1


@patch('page_loader.scripts.page_loader.create_parser')
def test_script_page_loader_exit4(cp_mock):
    fixt = get_path_fixture('empty.html')
    cp_mock.return_value = OK_URL, FAKE_LINKS['error_dir1']
    with requests_mock.Mocker() as m:
        m.get(OK_URL, text=open(fixt, 'r').read(), status_code=200)
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 1


@patch('page_loader.scripts.page_loader.create_parser')
def test_script_page_loader_exit5(cp_mock):
    dir_name = FAKE_LINKS['dir_for_resources']
    fixt = get_path_fixture('empty.html')
    with tempfile.TemporaryDirectory() as t:
        cp_mock.return_value = OK_URL, t
        os.mkdir(os.path.join(t, dir_name))
        with requests_mock.Mocker() as m:
            m.get(OK_URL, text=open(fixt, 'r').read(), status_code=200)
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 2
