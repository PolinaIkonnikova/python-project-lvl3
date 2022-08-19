import requests
from urllib.parse import urlparse
from .aux.logs_config import logger
from .aux.print_message import traceback_message
from .aux.custom_exceptions import CommonPageLoaderException


def request_http(url, bytes=False):
    try:
        r = requests.get(url)
        status_code = r.status_code
        if status_code != 200:
            logger.warning(f"The response code of {url} is {status_code}, "
                           "the page didn't load")
            raise CommonPageLoaderException(str(status_code))
        if bytes is True:
            method = r.content
        else:
            method = r.text
        return method
    except (requests.exceptions.InvalidURL,
            requests.exceptions.InvalidSchema,
            requests.exceptions.MissingSchema) as e:
        logger.warning(f'The invalid url {url}:\n'
                       f'{traceback_message(e)}')
        raise
    except requests.RequestException as e:
        logger.warning(f'{url} requests exception:\n'
                       f'{traceback_message(e)}')
        raise


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def valid_link(link, parent_url):
    if not urlparse(link).netloc:
        return urlparse(parent_url)._replace(path=link).geturl()
    return link
