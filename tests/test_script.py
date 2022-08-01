import requests_mock
import pytest
from page_loader.scripts.page_loader_script import download_page, main
from tests.fixtures.stubs_and_fixt import get_abs_path_fixture, FAKE_LINKS
from page_loader.aux.custom_exceptions import CommonPageLoaderException


def test_downloading_page_with_wrong_args():
    url = FAKE_LINKS['invalid_url2']
    fixt = get_abs_path_fixture('just_file.txt')
    dir = FAKE_LINKS['home']
    with requests_mock.Mocker() as m:
        m.get(url, text=open(fixt, 'r').read(), status_code=404)
        with pytest.raises(CommonPageLoaderException):
            download_page(url, dir)


@pytest.mark.parametrize('url, dir', [
                         (FAKE_LINKS['invalid_url1'], FAKE_LINKS['home']),
                         (FAKE_LINKS['invalid_url3'], FAKE_LINKS['home']),
                         (FAKE_LINKS['normal_url'], FAKE_LINKS['error_dir1'])
                         ])
def test_main_with_wrong_args(url, dir):
    def fake_args():
        return url, dir
    with pytest.raises(SystemExit) as e:
        main(get_args=fake_args)
        assert e.value.code == 1



# def fake_parser():
#     url = ''
#     fake_d = 'ololo'
#     return url, fake_d
#
#
# def test_script_page_loader_exit2():
#     with pytest.raises(SystemExit) as e:
#         main(get_args=fake_parser)
#     assert e.value.code == 1
#
#
# def test_script_page_loader_exit4():
#     with pytest.raises(SystemExit) as e:
#         main()
#     assert e.value.code == 1
#
#
# def test_script_page_loader_exit0():
#     with tempfile.TemporaryDirectory() as temp:
#
#         with requests_mock.Mocker() as m:
#             url = 'https://ru.hexlet.io/courses'
#             fixt = 'fixtures/just_file.txt'
#
#             def fake_args(*args):
#                 url, temp = args
#
#                 return url, temp
#
#             m.get(url, text=open(fixt, 'r').read(), status_code=200)
#             create_parser = fake_args
#             main()
#             assert os.path.exists(os.path.join(temp, 'ru-hexlet-io-courses.html'))
#             assert os.path.exists(os.path.join(temp, 'ru-hexlet-io-courses_files'))
#
#
#
# def test_script_page_loader_exit1():
#     with tempfile.TemporaryDirectory() as temp:
#
#         with requests_mock.Mocker() as m:
#             url = 'https://ru.hexlet.io/courses'
#             fixt = 'fixtures/just_file.txt'
#
#             def fake_args():
#                 return url, temp
#
#             m.get(url, text=open(fixt, 'r').read(), status_code=400)
#             with pytest.raises(SystemExit) as e:
#                 main(get_args=fake_args)
#                 assert e.value.code == 1