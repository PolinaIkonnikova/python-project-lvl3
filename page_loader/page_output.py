import os
import requests
from .name_generator import true_name, name_dir
from .page_parser import get_resources


def download(url, output_path='home_path'):
    if output_path == 'home_path':
        output_path = os.getcwd()
    name_new_dir = name_dir(url, output_path)
    os.mkdir(name_new_dir)
    new_page = true_name(url, is_html=True)
    path_page = os.path.join(output_path, new_page)
    r = requests.get(url)
    with open(path_page, 'w') as p:
        p.write(r.text)
    #get_resources(path_page, url, name_new_dir)
    #get_links(path_page, url, name_new_dir)
    #get_scripts(path_page, url, name_new_dir)
    return path_page
