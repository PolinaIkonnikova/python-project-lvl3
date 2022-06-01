import os
import requests
import logging
import sys
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs
from .name_generator import true_name, make_path

logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s - %(asctime)s')
logger1 = logging.getLogger(__name__)


def make_page(url, output_path):
    new_page_path = os.path.join(output_path, true_name(url))
    return new_page_path


def writing_page(url, new_page_path):
    try:
        r = requests.get(url)
    except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
        print('HTTP error occured. Seems this is not a page!')
        sys.exit()
    except requests.exceptions.ConnectionError:
        print('Connection failed, try again!')
        sys.exit()

    with open(new_page_path, 'w') as p:
        p.write(r.text)


def make_dir(url, output_path):
    new_dir_path = os.path.join(output_path, true_name(url, is_dir=True))
    try:
        os.mkdir(new_dir_path)
    except (FileNotFoundError, NotADirectoryError):
        print("This directory doesn't exist. Please change another dir!")
        sys.exit(1)
    except PermissionError:
        print("You doesn't have access rights, please choose another dir")
        sys.exit(1)
    return new_dir_path


def download_source(path, url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            logger1.info(f'something went wrong, a response code {r.status_code}')
        else:
            with open(path, 'wb') as p:
                p.write(r.content)
    except requests.RequestException:
        print('Something went wrong')


def get_resources(html_page, parent_url, dir_path, downloading=download_source):
    resource_dict = {'img': 'src', 'link': 'href', 'script': 'src'}
    with open(html_page, 'r') as hp:
        soup = bs(hp.read(), features="html.parser")
        for teg, atr in resource_dict.items():
            resource_list = soup.find_all(teg, attrs={atr: True})
            for res in resource_list:
                source = res[atr]

                if not urlparse(source).netloc:
                    source = urljoin(parent_url, source)

                if urlparse(source).netloc != urlparse(parent_url).netloc:
                    continue
                res_name = true_name(source)
                res_path = make_path(dir_path, res_name)
                downloading(res_path, source)
                res[atr] = res_path
    with open(html_page, 'w') as hp:
        hp.write(soup.prettify())


def download(url, output_path='home_path', downloading_res = get_resources):
    if output_path == 'home_path':
        output_path = os.getcwd()

    new_dir = make_dir(url, output_path)
    #logger1.info("that's a new dir - {}".format(name_new_dir))
    new_page_path = make_page(url, output_path)
    #logger1.info("that's a new page - {}".format(new_page))
    writing_page(url, new_page_path)

    #downloading_res(new_page_path, url, new_dir)
    return new_page_path


