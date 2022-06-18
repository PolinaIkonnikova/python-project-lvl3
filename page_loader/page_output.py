import os
import requests
import sys
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs
from .name_generator import true_name, make_path
from .logs.logs_config import logger, err_logger


def make_page(url, output_path):
    new_page_path = os.path.join(output_path, true_name(url))
    return new_page_path


def writing_page(url, new_page_path):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            logger.warning(f'Something went wrong, a response code is {r.status_code}')
        with open(new_page_path, 'w') as p:
            p.write(r.text)
    except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
        err_logger.error('HTTP error occured. Seems this is not a page!')
        sys.exit()
    except requests.exceptions.ConnectionError:
        err_logger.error('Connection failed, try again!')
        sys.exit()


def make_dir(url, output_path):
    new_dir_path = os.path.join(output_path, true_name(url, is_dir=True))
    try:
        os.mkdir(new_dir_path)
    except (FileNotFoundError, NotADirectoryError):
        err_logger.error("This directory doesn't exist. Please change another dir!")
        sys.exit(1)
    except PermissionError:
        err_logger.error("You doesn't have access rights, please choose another dir")
        sys.exit(1)
    return new_dir_path


def download_source(path, url):
    try:
        r = requests.get(url)
        with open(path, 'wb') as p:
            p.write(r.content)
    except requests.RequestException:
        err_logger.error('Something went wrong')
        sys.exit(1)


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


def download(url, output_path, downloading_res=get_resources):
    if output_path == 'home_path':
        output_path = os.getcwd()

    new_page_path = make_page(url, output_path)
    writing_page(url, new_page_path)
    logger.debug(f"that's a new page - {new_page_path}")

    try:
        new_dir = make_dir(url, output_path)
        logger.debug(f"that's a new dir for page's resources - {new_dir}")
    except FileExistsError:
        err_logger.error("The directory with page's files exists yet!")
        sys.exit()

    #downloading_res(new_page_path, url, new_dir)
    return err_logger.debug(f'successfull downloading {new_page_path}')

