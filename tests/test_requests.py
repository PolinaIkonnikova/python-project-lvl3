import requests_mock
import requests
import tempfile
import pytest
from page_loader.page_output import download_page
from page_loader.for_http import request_http
from page_loader.aux.custom_exceptions import CommonPageLoaderException
from .fixtures.for_fixtures import FAKE_LINKS, get_path_fixture


FAKE_URL = FAKE_LINKS['invalid_url1']


def test_requests_http():
    fixt = get_path_fixture('just_file.txt')
    with requests_mock.Mocker() as m:
        m.get(FAKE_URL, text=open(fixt, 'r').read(), status_code=200)
        assert request_http(FAKE_URL) == 'hello'
# def test_loading_res():
#     fixt = get_path_fixture("site-com-blog-about-assets-styles.css")
#     with tempfile.TemporaryDirectory() as t:
#         res_description = {'tag': 'link',
#                            'source': "https://some_file.js",
#                            'res_path': 'some_file.scc'}
#         with requests_mock.Mocker() as m:
#             m.get("https://some_file.js", text=open(fixt, 'r').read(),
#                   status_code=200)
#             load_res(res_description, t)
#         file = os.path.join(t, 'some_file.scc')
#
#         with open(file, 'rb') as f:
#             assert f.read() == b'\xef\xbb\xbfh3 { font-weight: normal; }\n'


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


def test_download_page_mistakes3():
    with pytest.raises(CommonPageLoaderException):
        with tempfile.TemporaryDirectory() as temp:
            download_page(FAKE_URL, temp)
