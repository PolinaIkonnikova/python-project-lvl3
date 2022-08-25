import requests_mock
import requests
import pytest
from page_loader.http import request_http
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from .fixtures.for_fixtures import FAKE_LINKS, get_path_fixture


FAKE_URL = FAKE_LINKS['invalid_url1']


def test_requests_http2():
    with pytest.raises(requests.exceptions.InvalidSchema):
        request_http(FAKE_URL)
    with pytest.raises(requests.exceptions.ConnectionError):
        request_http(FAKE_LINKS['invalid_url2'])
    with pytest.raises(requests.exceptions.MissingSchema):
        request_http(FAKE_LINKS['invalid_url3'])


def test_requests_http3():
    fixt = get_path_fixture('just_file.txt')
    with requests_mock.Mocker() as m:
        m.get(FAKE_URL, text=open(fixt, 'r').read(), status_code=500)
        with pytest.raises(CommonPageLoaderException):
            request_http(FAKE_URL)
