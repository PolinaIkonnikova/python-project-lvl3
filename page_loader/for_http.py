import requests
import sys
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs
from .work_with_files import true_name, make_path
from .progress_bar import download_progress
from .logs.logs_config import make_logger


logger = make_logger()


def request_http(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r
    elif r.status_code == 403:
        #логируем описание запрещенный контент
        raise requests.exceptions.HTTPError
    elif r.status_code == 404: # все запросы 300
        # логируем описание страница не найдена
        raise requests.exceptions.HTTPError
    elif r.status_code == 500: # все запросы 500
        # логируем описание ошибка серера
        raise requests.exceptions.HTTPError


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def valid_link(link, parent_url):
    if not urlparse(link).netloc:
        link = urljoin(parent_url, link)
    return link


def writing(file, data, bytes=False):
    if bytes is True:
        tag = 'wb'
        method = data.content
    else:
        tag = 'w'
        method = data.text

    with open(file, tag) as f:
        f.write(method)