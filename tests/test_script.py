import os
import requests_mock
import pytest
import tempfile
from page_loader.scripts.page_loader import downloading, main
from tests.fixtures.stubs_and_fixt import get_abs_path_fixture, FAKE_LINKS
from page_loader.aux.custom_exceptions import CommonPageLoaderException

ok_url = FAKE_LINKS['normal_url']
fixt = get_abs_path_fixture('empty.html')


def test_script_page_loader_exit1():
    with tempfile.TemporaryDirectory() as t:
        #new_html_name = FAKE_LINKS['new_html_name']
        png_source = 'https://ru.hexlet.io/assets/professions/nodejs.png'
        fixt1 = get_abs_path_fixture('one_png.html')
        fixt2 = get_abs_path_fixture('just_file.txt')
        with requests_mock.Mocker() as m:
            m.get(ok_url, text=open(fixt1, 'r').read(), status_code=200)
            m.get(png_source, text=open(fixt2, 'r').read(), status_code=404)
            with pytest.raises(SystemExit) as e:
                downloading(ok_url, t)
            assert e.value.code == 0


def test_script_page_loader_exit2():
    with tempfile.TemporaryDirectory() as t:
        with requests_mock.Mocker() as m:
            m.get(ok_url, text=open(fixt, 'r').read(), status_code=200)
            with pytest.raises(SystemExit) as e:
                downloading(ok_url, t)
            assert e.value.code == 0


def test_script_page_loader_exit3():
    with tempfile.TemporaryDirectory() as t:
        with requests_mock.Mocker() as m:
            m.get(ok_url, text=open(fixt, 'r').read(), status_code=500)
            with pytest.raises(SystemExit) as e:
                downloading(ok_url, t)
            assert e.value.code == 1


@pytest.mark.parametrize('warning_url', [FAKE_LINKS['invalid_url1'],
                                         FAKE_LINKS['invalid_url3'],
                                         FAKE_LINKS['invalid_url4']])
def test_script_page_loader_exit4(warning_url):
    with tempfile.TemporaryDirectory() as t:
        with pytest.raises(SystemExit) as e:
            downloading(warning_url, t)
        assert e.value.code == 1


def test_script_page_loader_exit5():
    with requests_mock.Mocker() as m:
        m.get(ok_url, text=open(fixt, 'r').read(), status_code=200)
        with pytest.raises(SystemExit) as e:
            downloading(ok_url, FAKE_LINKS['error_dir1'])
        assert e.value.code == 1


def test_script_page_loader_exit6():
    dir_name = FAKE_LINKS['dir_for_resources']
    with tempfile.TemporaryDirectory() as t:
        os.mkdir(os.path.join(t, dir_name))
        with requests_mock.Mocker() as m:
            m.get(ok_url, text=open(fixt, 'r').read(), status_code=200)
            with pytest.raises(SystemExit) as e:
                downloading(ok_url, t)
            assert e.value.code == 2
