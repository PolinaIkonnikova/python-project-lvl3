import os
import re
from urllib.parse import urlparse


def name_dir(url, output_path):
    new_dir_name = true_name(url, is_dir=True)
    return os.path.join(output_path, new_dir_name)


def make_path(output_path, file_name):
    return os.path.join(output_path, file_name)


def true_name(url, is_dir=False, is_html=False):
    path_part, ending = os.path.splitext(url)
    if is_dir is True:
        ending = '_files'
    if is_html is True:
        ending = '.html'
    path_body = urlparse(path_part).netloc + urlparse(path_part).path
    return '-'.join(re.findall(r'\w+', path_body)) + ending



