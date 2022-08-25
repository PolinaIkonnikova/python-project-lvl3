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


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def valid_link(link, parent_url):
    return urljoin(parent_url, link)
