import os
import re
from .aux.print_message import traceback_message
from urllib.parse import urlparse
from .aux.logs_config import logger
from .aux.custom_exceptions import CommonPageLoaderException


def valid_dir(output_path):
    try:
        if not os.path.isdir(output_path):
            logger.error(f'{output_path} is not a directory.')
            raise CommonPageLoaderException('not found dir')
        if not os.access(output_path, os.R_OK & os.W_OK & os.X_OK):
            logger.error(f'No permissions for {output_path}.')
            raise CommonPageLoaderException('no permissions')
        return output_path
    except (FileNotFoundError, FileExistsError) as e:
        logger.error(f'The directory {output_path} not found:\n'
                     f'{traceback_message(e)}')
        raise CommonPageLoaderException('not found dir')


def make_path(output_path, file_name):
    return os.path.join(output_path, file_name)


def make_name(url, is_dir=False):
    path_part, ending = os.path.splitext(url)
    if is_dir is True:
        ending = '_files'
    if not ending:
        ending = '.html'
    path_body = urlparse(path_part).netloc + urlparse(path_part).path
    return '-'.join(re.findall(r'\w+', path_body)) + ending


def prepare_dir(url, output_path):
    dir_name = make_name(url, is_dir=True)
    dir_path = make_path(output_path, dir_name)
    try:
        os.mkdir(dir_path)
        return dir_name, dir_path
    except FileExistsError as e:
        logger.error('File exist error:'
                     f'{traceback_message(e)}')
        raise


def write_file(file, data):
    try:
        with open(file, 'wb') as f:
            f.write(data)
    except PermissionError as e:
        logger.warning(f'{file} permission error for writing:\n'
                       f'{traceback_message(e)}')
        raise
