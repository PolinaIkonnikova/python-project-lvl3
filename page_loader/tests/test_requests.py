import os
import requests_mock
import tempfile
import pytest
from page_loader.page_output import download_page
from page_loader.aux.custom_exceptions import RequestsError
from page_loader.for_http import request_http
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from page_loader.tests.fixtures.stubs_and_fixt import FAKE_LINKS


url = FAKE_LINKS['invalid_url1']
# @pytest.mark.parametrize('wrong_url', ['htps://ru.hexlet.io/courses', 'some_dir.png', '/ru.hexlet.io/courses.html'])
# def test_requests_http1(wrong_url):
#     with pytest.raises(RequestsError):
#         request_http(wrong_url)


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
            new_page = download_page(url, temp)


def test_requests_http1():
    with requests_mock.Mocker() as m:
        m.get(url, status_code=500)
        with pytest.raises(RequestsError) as e:
            request_http(url)
            print(e)
