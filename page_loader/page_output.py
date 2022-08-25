import os.path
import requests
from page_loader.http import request_http
from .work_with_files import make_name, make_path, write_file
from .aux.logs_config import logger
from .aux.custom_exceptions import CommonPageLoaderException
from page_loader.urls_and_bs import get_soup, save_html_changes,\
    valid_link, is_parent_netloc
from page_loader.work_with_files import prepare_dir, valid_dir
from .aux.print_message import traceback_message
from page_loader.progress_bar import download_progress


RES_TAGS = {'img': 'src', 'link': 'href', 'script': 'src'}


def download_page(page_path, url):
    content = request_http(url)
    write_file(page_path, content)


def get_resources(html_page, parent_url):
    all_resources = list(map(lambda tag, atr:
                             html_page.find_all(tag, attrs={atr: True}),
                             RES_TAGS.keys(), RES_TAGS.values()))

    filter_resources = list(filter(lambda res:
                                   is_parent_netloc(res[RES_TAGS[res.name]],
                                                    parent_url),
                                   sum(all_resources, [])))
    return filter_resources


def download(url, output_path):
    logger.info(f'Start data:\n - url: {url}\n'
                f' - path: {output_path}')
    output_path = valid_dir(output_path)
    page_path = make_path(output_path, make_name(url))

    try:
        download_page(page_path, url)
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

    logger.info('The page recording completed. '
                'Starting to work with resources.\n')

    dir_name, dir_path = prepare_dir(url, output_path)
    logger.info('The directory for resources '
                f'is {os.path.abspath(dir_path)}')
    html_page = get_soup(page_path)
    resources = get_resources(html_page, url)

    with download_progress(len(resources)) as p:
        for res in resources:
            p.next()
            source_atr = RES_TAGS[res.name]
            res_url = valid_link(res[source_atr], url)
            res_name = make_name(res_url)
            try:
                download_page(make_path(dir_path, res_name), res_url)
                logger.info(f'The resource {res_url} has loaded')
            except (PermissionError, CommonPageLoaderException,
                    requests.RequestException):
                pass
            except Exception as e:
                logger.warning(f'Unexpected wrong with resourse {res_url}, '
                               f'not downloaded:\n{traceback_message(e)}')
                continue
            else:
                res[source_atr] = make_path(dir_name, res_name)

    save_html_changes(page_path, html_page)
    logger.info(f'The page {page_path} has loaded.')
    return page_path
