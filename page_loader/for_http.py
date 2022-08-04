import requests
from urllib.parse import urlparse
from page_loader.aux.custom_exceptions import CommonRequestsError
from page_loader.aux.logs_config import mistake_logger

logger = mistake_logger(__name__)


def request_http(url, bytes=False):
    try:
        r = requests.get(url)
        status_code = r.status_code
        if status_code != 200:
            logger.debug(f'Ресурс {url} не скачан, '
                         f'код ответа сервера - {status_code}.')
            raise CommonRequestsError(url=url, code=status_code)
        if bytes is True:
            method = r.content
        else:
            method = r.text
        logger.debug(f'Данные с {url} отправлены на запись')
        return method
    except (requests.exceptions.InvalidURL,
            requests.exceptions.InvalidSchema,
            requests.exceptions.MissingSchema):
        message = f'Неверый адрес страницы {url}, ресурс не скачан.'
        logger.debug(message)
        raise CommonRequestsError(url=url,
                                  error=message)
    except requests.exceptions.ConnectionError as e:
        message = f'С {url} произошла неприятность : {e}'
        logger.debug(message)
        raise CommonRequestsError(url=url, error=message)


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def valid_link(link, parent_url):
    if not urlparse(link).netloc:
        return urlparse(parent_url)._replace(path=link).geturl()
    return link
