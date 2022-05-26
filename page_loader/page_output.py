import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from .name_generator import true_name, name_dir, make_path


def download_source(path, url):
    with open(path, 'wb') as p:
        p.write(requests.get(url).content)


def get_resources(html_page, parent_url, dir_path):
    resource_dict = {'img': 'src', 'link': 'href', 'script': 'src'}
    with open(html_page, 'r') as hp:
        soup = bs(hp.read(), features="html.parser")
        for teg, atr in resource_dict.items():
            resource_list = soup.find_all(teg, attrs={atr: True})
            for res in resource_list:
                source = res[atr]
                if not urlparse(source).netloc:
                    source = parent_url + source
                if urlparse(source).netloc != urlparse(parent_url).netloc:
                    continue
                res_name = true_name(source)
                res_path = make_path(dir_path, res_name)
                download_source(res_name, res_path)
                teg[atr] = res_path
    with open(html_page, 'w') as hp:
        hp.write(soup.prettify())


def download(url, output_path='home_path'):
    if output_path == 'home_path':
        output_path = os.getcwd()
    name_new_dir = name_dir(url, output_path)
    os.mkdir(name_new_dir)
    new_page = true_name(url)
    path_page = os.path.join(output_path, new_page)
    r = requests.get(url)
    with open(path_page, 'w') as p:
        p.write(r.text)
    get_resources(path_page, url, name_new_dir)

