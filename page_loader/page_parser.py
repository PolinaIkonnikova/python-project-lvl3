import requests
from bs4 import BeautifulSoup as bs
from .name_generator import true_name, make_path
from urllib.parse import urlparse


def download_source(path, url):
    with open(path, 'wb') as p:
        p.write(requests.get(url).content)


def get_resources(html_page, parent_url, dir_path):
    resource_dict = {'img': 'src', 'link': 'href', 'script': 'src'}
    i = 0
    with open(html_page, 'r') as hp:
        soup = bs(hp.read(), features="html.parser")
        for teg, atr in resource_dict.items():
            #resource_list = soup.find_all(teg)
            for res in soup.find_all(teg):
                i += 1
    return i


def get_images(html_page, parent_url, dir_path):
    with open(html_page, 'r') as hp:
        soup = bs(hp.read(), features="html.parser")
        for image in soup.find_all('img'):
            image_source = image['src']
            if not urlparse(image_source).scheme and not urlparse(image_source).netloc:
                image_source = parent_url + image_source
            image_name = true_name(image_source)
            image_path = make_path(dir_path, image_name)
            download_source(image_path, image_source)
            image['src'] = image_path
    with open(html_page, 'w') as hp:
        hp.write(soup.prettify())


def get_links(html_page, parent_url, dir_path):
    with open(html_page, 'r') as hp:
        soup = bs(hp.read(), features="html.parser")
        for link in soup.find_all('link'):
            link_source = link['href']
            if not urlparse(link_source).scheme and not urlparse(link_source).netloc:
                link_source = parent_url + link_source
            link_name = true_name(link_source)
            link_path = make_path(dir_path, link_name)
            download_source(link_path, link_source)
            link['src'] = link_path
    with open(html_page, 'w') as hp:
        hp.write(soup.prettify())


def get_scripts(html_page, parent_url, dir_path):
    with open(html_page, 'r') as hp:
        soup = bs(hp.read(), features="html.parser")
        for script in soup.find_all('script'):
            script_source = script['src']
            if not urlparse(script_source).scheme and not urlparse(script_source).netloc:
                script_source = parent_url + script_source
            script_name = true_name(script_source)
            script_path = make_path(dir_path, script_name)
            download_source(script_path, script_source)
            script['src'] = script_path
    with open(html_page, 'w') as hp:
        hp.write(soup.prettify())


def html_parsing(html, url):
    with open(html, 'r') as h:
        soup = bs(h.read(), features="html.parser")
        return parse_pictures(soup, url)


def parse_pictures(soup, url):
    images = soup.find_all('img')
    for image in images:
        image['src'] = make_path(url, 'image_jpg')
        print(image)

