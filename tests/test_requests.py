import requests_mock
import tempfile
import pytest
from page_loader.page_output import download_page
from page_loader.for_http import request_http
from page_loader.aux.custom_exceptions import CommonPageLoaderException, CommonRequestsError
from tests.fixtures.stubs_and_fixt import FAKE_LINKS, get_abs_path_fixture


fake_url = FAKE_LINKS['invalid_url1']
fixt = get_abs_path_fixture('just_file.txt')


def test_requests_http1():
    with requests_mock.Mocker() as m:
        m.get(fake_url, text=open(fixt, 'r').read(), status_code=200)
        assert request_http(fake_url) == 'hello'
        assert request_http(fake_url, bytes=True) == b'hello'


@pytest.mark.parametrize('wrong_url', [fake_url, FAKE_LINKS['invalid_url2'],
                                       FAKE_LINKS['invalid_url3'], FAKE_LINKS['invalid_url4']])
def test_requests_http2(wrong_url):
    with pytest.raises(CommonRequestsError):
        request_http(wrong_url)


def test_requests_http3():
    with requests_mock.Mocker() as m:
        m.get(fake_url, text=open(fixt, 'r').read(), status_code=500)
        with pytest.raises(CommonRequestsError):
            request_http(fake_url)


# def test_download_page_mistakes():
#     with requests_mock.Mocker() as m:
#         url = 'https://ru.hexlet.io/courses'
#         fixt = 'fixtures/just_file.txt'
#         m.get(url, text=open(fixt, 'r').read(), status_code=200)
#         with tempfile.TemporaryDirectory() as temp:
#             new_page = download_page(url, temp)
#             assert os.path.exists(new_page)
#
#
# def test_download_page_mistakes2():
#     with requests_mock.Mocker() as m:
#         url = 'https://ru.hexlet.io/courses'
#         fixt = 'fixtures/just_file.txt'
#         m.get(url, status_code=300)
#         with pytest.raises(CommonPageLoaderException):
#             with tempfile.TemporaryDirectory() as temp:
#                 new_page = download_page(url, temp)
            #assert str(e.value) == 'expected message from exception'

def test_download_page_mistakes3():
    with pytest.raises(CommonPageLoaderException):
        with tempfile.TemporaryDirectory() as temp:
            download_page(fake_url, temp)
