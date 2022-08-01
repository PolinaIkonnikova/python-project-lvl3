import os
import re
from urllib.parse import urlparse
from .aux.logs_config import mistakes_logging
from .aux.custom_exceptions import CommonPageLoaderException


def home_dir():
    return os.path.expanduser(os.getenv('HOME'))


def valid_dir(output_path):
    if output_path == 'home_path':
        output_path = home_dir()
    if not os.path.isdir(output_path):
        #логирование
        raise NotADirectoryError
    if not os.access(output_path, os.R_OK & os.W_OK & os.X_OK):
        #логирование
        raise PermissionError
    return output_path


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
    try:
        os.mkdir(new_dir)
        return new_dir
    except FileExistsError:
        #mistakes_logging(e, 5, new_dir)
        raise CommonPageLoaderException


def writing(file, data, bytes=False):
    if bytes is True:
        tag = 'wb'
    else:
        tag = 'w'
    with open(file, tag) as f:
        f.write(data)