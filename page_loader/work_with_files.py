import os
import re
from urllib.parse import urlparse
from .aux.logs_config import logging_message
from .aux.custom_exceptions import CommonPageLoaderException


def valid_dir(output_path):
    try:
        if not os.path.isdir(output_path):
            logging_message('Кажется, выбранная директория'
                            ' не существует или не директория вовсе!',
                            error=True)
            raise CommonPageLoaderException
        if not os.access(output_path, os.R_OK & os.W_OK & os.X_OK):
            logging_message('Придется выбрать другую директорию, '
                            'малыш, ты еще слишком мал для использования этой.',
                            error=True)
            raise CommonPageLoaderException
        return output_path
    except (FileNotFoundError, FileExistsError) as e:
        logging_message('Что-то не так с выбранной директорией, '
                        f'выбирай другую: {e}', error=True)
        raise CommonPageLoaderException


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
    dir_name = true_name(url, is_dir=True)
    dir_path = make_path(output_path, true_name(url, is_dir=True))
    try:
        os.mkdir(dir_path)
        return dir_name, dir_path
    except FileExistsError:
        logging_message(f'Папка для ресурсов {dir_path} существует,\n'
                        f'возможно, страница {url} уже скачана. '
                        f'Стоит перепроверить!',
                        error=True)
        raise


def writing(file, data, bytes=False):
    if bytes is True:
        tag = 'wb'
    else:
        tag = 'w'
    try:
        with open(file, tag) as f:
            f.write(data)
    except PermissionError:
        logging_message('Ошибка прав доступа, придется выбрать'
                        'другую директорию!', error=True)
        raise CommonPageLoaderException
