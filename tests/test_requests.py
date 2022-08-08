import requests_mock
import tempfile
import pytest
from page_loader.page_output import download_page
from page_loader.for_http import request_http
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from page_loader.aux.custom_exceptions import CommonRequestsError
from tests.fixtures.for_fixtures import FAKE_LINKS, get_path_fixture


FAKE_URL = FAKE_LINKS['invalid_url1']


def test_requests_http():
    fixt = get_path_fixture('just_file.txt')
    with requests_mock.Mocker() as m:
        m.get(FAKE_URL, text=open(fixt, 'r').read(), status_code=200)
        assert request_http(FAKE_URL) == 'hello'


def test_requests_http_bytes():
    fixt = get_path_fixture('site-com-blog-about-assets-styles.css')
    with requests_mock.Mocker() as m:
        m.get(FAKE_URL, text=open(fixt, 'r').read(), status_code=200)
        assert request_http(FAKE_URL, bytes=True) == b'\xef\xbb\xbfh3 { font-weight: normal; }\n'


@pytest.mark.parametrize('wrong_url', [FAKE_URL, FAKE_LINKS['invalid_url2'],
                                       FAKE_LINKS['invalid_url3'],
                                       FAKE_LINKS['invalid_url4']])
def test_requests_http2(wrong_url):
    with pytest.raises(CommonRequestsError):
        request_http(wrong_url)


def test_requests_http3():
    fixt = get_path_fixture('just_file.txt')
    with requests_mock.Mocker() as m:
        m.get(FAKE_URL, text=open(fixt, 'r').read(), status_code=500)
        with pytest.raises(CommonRequestsError):
            request_http(FAKE_URL)


def test_download_page_mistakes3():
    with pytest.raises(CommonPageLoaderException):
        with tempfile.TemporaryDirectory() as temp:
            download_page(FAKE_URL, temp)
