import os
import requests_mock
import pytest
import tempfile
from page_loader.scripts.page_loader import main
from tests.fixtures.for_fixtures import FAKE_LINKS, get_path_fixture


OK_URL = FAKE_LINKS['normal_url']


def test_script_page_loader_exit1():
    with tempfile.TemporaryDirectory() as t:
        png_source = 'https://ru.hexlet.io/assets/professions/nodejs.png'
        fixt1 = get_path_fixture('one_png.html')
        fixt2 = get_path_fixture('just_file.txt')

        def fake_parser():
            return OK_URL, t

        with requests_mock.Mocker() as m:
            m.get(OK_URL, text=open(fixt1, 'r').read(), status_code=200)
            m.get(png_source, text=open(fixt2, 'r').read(), status_code=404)
            with pytest.raises(SystemExit) as e:
                main(get_args=fake_parser)
            assert e.value.code == 0


def test_script_page_loader_exit2():
    fixt = get_path_fixture('empty.html')
    with tempfile.TemporaryDirectory() as t:

        def fake_parser():
            return OK_URL, t

        with requests_mock.Mocker() as m:
            m.get(OK_URL, text=open(fixt, 'r').read(), status_code=500)
            with pytest.raises(SystemExit) as e:
                main(get_args=fake_parser)
            assert e.value.code == 1


@pytest.mark.parametrize('warning_url', [FAKE_LINKS['invalid_url1'],
                                         FAKE_LINKS['invalid_url3'],
                                         FAKE_LINKS['invalid_url4']])
def test_script_page_loader_exit3(warning_url):
    with tempfile.TemporaryDirectory() as t:

        def fake_parser():
            return warning_url, t

        with pytest.raises(SystemExit) as e:
            main(get_args=fake_parser)
        assert e.value.code == 1


def test_script_page_loader_exit4():
    fixt = get_path_fixture('empty.html')

    def fake_parser():
        return OK_URL, FAKE_LINKS['error_dir1']

    with requests_mock.Mocker() as m:
        m.get(OK_URL, text=open(fixt, 'r').read(), status_code=200)
        with pytest.raises(SystemExit) as e:
            main(get_args=fake_parser)
        assert e.value.code == 1


def test_script_page_loader_exit5():
    dir_name = FAKE_LINKS['dir_for_resources']
    fixt = get_path_fixture('empty.html')

    with tempfile.TemporaryDirectory() as t:

        def fake_parser():
            return OK_URL, t

        os.mkdir(os.path.join(t, dir_name))
        with requests_mock.Mocker() as m:
            m.get(OK_URL, text=open(fixt, 'r').read(), status_code=200)
            with pytest.raises(SystemExit) as e:
                main(get_args=fake_parser)
            assert e.value.code == 2
