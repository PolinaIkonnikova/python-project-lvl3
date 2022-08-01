import os
import requests
from urllib.parse import urlparse, urljoin, urlsplit
from page_loader.aux.custom_exceptions import CommonRequestsError
from page_loader.aux.logs_config import mistakes_logging


def request_http(url, bytes=False):
    try:
        r = requests.get(url)
        status_code = r.status_code
        if status_code != 200:
            raise CommonRequestsError(url=url, s_code=status_code)

        if bytes is True:
            method = r.content
        else:
            method = r.text
        return method
    except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema,
            requests.exceptions.MissingSchema) as e:
        raise CommonRequestsError(url=url, error=e)
    except requests.exceptions.ConnectionError as e:
        raise CommonRequestsError(url=url, error=e)



def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def valid_link(link, parent_url):
    if not urlparse(link).netloc:
        return urlparse(parent_url)._replace(path=link).geturl()
    return link

