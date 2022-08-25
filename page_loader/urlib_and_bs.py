import os
import re
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, urljoin


def get_soup(page_path):
    with open(page_path, 'r', encoding='utf-8') as hp:
        soup = bs(hp.read(), features="html.parser")
    return soup


def save_html_changes(page_path, html):
    with open(page_path, 'w') as hp:
        hp.write(html.prettify())


def is_parent_netloc(url, parent_url):
    cond1 = urlparse(url).netloc
    cond2 = urlparse(url).netloc != urlparse(parent_url).netloc
    return not(cond1 and cond2)


def valid_link(link, parent_url):
    return urljoin(parent_url, link)


def make_name(url, is_dir=False):
    path_part, ending = os.path.splitext(url)
    if is_dir is True:
        ending = '_files'
    if not ending:
        ending = '.html'
    path_body = urlparse(path_part).netloc + urlparse(path_part).path
    return '-'.join(re.findall(r'\w+', path_body)) + ending
