import requests
from page_loader.for_http import valid_link, request_http
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from page_loader.work_with_files import make_name,\
    make_path, write_file
from page_loader.aux.logs_config import logger
from .aux.print_message import traceback_message
from page_loader.progress_bar import download_progress
from page_loader.aux.custom_exceptions import CommonPageLoaderException


RES_TAGS = {'img': 'src', 'link': 'href', 'script': 'src'}


def is_parent_netloc(url, parent_url):
    cond1 = urlparse(url).netloc
    cond2 = urlparse(url).netloc != urlparse(parent_url).netloc
    return not(cond1 and cond2)


def make_res_name(source, dir_path):
    return make_path(dir_path, make_name(source))


def get_resources(soup, parent_url):
    all_resources = list(map(lambda tag, atr: soup.find_all(tag,
                                                            attrs={atr: True}),
                             RES_TAGS.keys(), RES_TAGS.values()))

    filter_resources = list(filter(lambda res:
                                   is_parent_netloc(res[RES_TAGS[res.name]],
                                                    parent_url),
                                   sum(all_resources, [])))
    return filter_resources


def download_resources(html_page, parent_url, dir_name, output_path):

    with open(html_page, 'r', encoding='utf-8') as hp:
        soup = bs(hp.read(), features="html.parser")
        all_resources = get_resources(soup, parent_url)

        if not all_resources:
            return

        with download_progress(len(all_resources)) as p:
            for res in all_resources:
                p.next()
                source = RES_TAGS[res.name]
                res_url = valid_link(res[source], parent_url)
                try:
                    data = request_http(res_url, bytes=True)
                    res_name = make_res_name(res_url, dir_name)
                    res_path = make_path(output_path, res_name)
                    write_file(res_path, data, bytes=True)
                    logger.info(f'The resource {res_url} has loaded')
                except (PermissionError, CommonPageLoaderException,
                        requests.RequestException):
                    continue
                except Exception as e:
                    logger.warning(f'Unexpected wrong with resourse {res_url}, '
                                   f'not downloaded:\n{traceback_message(e)}')
                    continue
                else:
                    res[source] = res_name

    with open(html_page, 'w') as hp:
        hp.write(soup.prettify())
