import os
import re
from urllib.parse import urlparse
from .aux.logs_config import mistake_logger
from .aux.custom_exceptions import CommonPageLoaderException


logger = mistake_logger(__name__)


def valid_dir(output_path):
    try:
        if not os.path.isdir(output_path):
            logger.warning('Кажется, выбранная директория'
                           ' не существует или не директория вовсе!')
            raise CommonPageLoaderException
        if not os.access(output_path, os.R_OK & os.W_OK & os.X_OK):
            logger.warning('Придется выбрать другую директорию, '
                           'малыш, ты еще слишком мал для использования этой.')
            raise CommonPageLoaderException
        return output_path
    except (FileNotFoundError, FileExistsError) as e:
        logger.warning('Что-то не так с выбранной директорией, '
                       f'выбирай другую: {e}')
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
    new_dir = make_path(output_path, true_name(url, is_dir=True))
    try:
        os.mkdir(new_dir)
        return new_dir
    except FileExistsError:
        logger.warning('Папка для ресурсов уже существует, '
                       'и возможно страница уже скачана. Стоит перепроверить!')
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
        logger.warning('Ошибка прав доступа, придется выбрать'
                       'другую директорию!')
        raise CommonPageLoaderException
