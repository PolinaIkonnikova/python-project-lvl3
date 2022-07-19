import os
import re
from urllib.parse import urlparse
from .logs.logs_config import make_logger


logger = make_logger()


def make_path(output_path, file_name):
    return os.path.join(output_path, file_name)


def true_name(url, is_dir=False):
    path_part, ending = os.path.splitext(url)
    if is_dir is True:
        ending = '_files'
    if not ending:
        ending = '.html'
    path_body = urlparse(path_part).netloc + urlparse(path_part).path
    return '-'.join(re.findall(r'\w+', path_body)) + ending


def prepare_dir(url, output_path):
    new_dir = make_path(output_path, true_name(url, is_dir=True))
    os.mkdir(new_dir)
    return new_dir
