import requests
from page_loader.aux.logs_config import logger
from page_loader.aux.print_message import traceback_message
from page_loader.aux.custom_exceptions import CommonPageLoaderException


def request_http(url):
    try:
        r = requests.get(url)
        status_code = r.status_code
        if status_code != 200:
            logger.warning(f"The response code of {url} is {status_code}, "
                           "the page didn't load")
            raise CommonPageLoaderException(str(status_code))
        return r.content
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
