import os.path
import requests
from .for_http import request_http
from .work_with_files import make_name, make_path, write_file
from .aux.logs_config import logger
from .aux.custom_exceptions import CommonPageLoaderException
from page_loader.resources_output import download_resources
from page_loader.work_with_files import prepare_dir, valid_dir


def download_page(url,
                  output_path,
                  get_content=request_http
                  ):
    try:
        new_html = make_path(output_path, make_name(url))
        content = get_content(url)
        write_file(new_html, content)
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
    logger.info(f'Start data:\nurl {url}\n'
                f'path {output_path}')
    output_path = valid_dir(output_path)
    page_path = download_page(url, output_path)
    logger.info('The page recording completed. '
                'Starting to work with resources.\n')
    dir_name, dir_path = prepare_dir(url, output_path)
    logger.info('The directory for resources '
                f'is {os.path.abspath(dir_path)}')
    download_resources(page_path, url, dir_name, output_path)
    logger.info(f'The page {page_path} has loaded.')
    return page_path
