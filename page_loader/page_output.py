import os.path
import requests
from .for_http import request_http
from .work_with_files import true_name, make_path, writing
from .aux.logs_config import logger
from .aux.print_message import user_friendly_message
from .aux.custom_exceptions import CommonPageLoaderException
from page_loader.resources_output import download_resources, get_resources
from page_loader.work_with_files import prepare_dir, valid_dir


def download_page(url,
                  output_path,
                  get_content=request_http
                  ):
    try:
        new_html = make_path(output_path, true_name(url))
        content = get_content(url)
        writing(new_html, content)
        return new_html
    except CommonPageLoaderException:
        raise
    except (requests.exceptions.InvalidURL,
            requests.exceptions.InvalidSchema,
            requests.exceptions.MissingSchema):
        raise CommonPageLoaderException('invalid url')
    except requests.RequestException:
        raise CommonPageLoaderException('request error')
    except PermissionError:
        raise CommonPageLoaderException('writing problem')


def download(url, output_path):
    try:
        logger.info(f'Start data:\nurl {url}\n'
                    f'path {output_path}')
        output_path = valid_dir(output_path)
        page_path = download_page(url, output_path)
        logger.info('The page recording completed. '
                    'Starting to work with resources.\n')
        dir_name, dir_path = prepare_dir(url, output_path)
        logger.info('The directory for resources '
                    f'is {dir_path}')
        user_friendly_message('resource dir', dir_path)
        resources = get_resources(page_path, url, dir_name)
        download_resources(resources, output_path)
        logger.info(f'The page {page_path} has loaded.')
        return page_path
    except CommonPageLoaderException as e:
        user_friendly_message(e.message)
        raise
    except FileExistsError:
        raise
