import os
from page_loader.for_http import valid_link, request_http
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from page_loader.work_with_files import true_name, make_path, writing
from page_loader.aux.logs_config import mistake_logger
from page_loader.progress_bar import download_progress
from page_loader.aux.custom_exceptions import CommonRequestsError

logger = mistake_logger(__name__)


def is_parent_netloc(url, parent_url):
    cond1 = urlparse(url).netloc
    cond2 = urlparse(url).netloc != urlparse(parent_url).netloc
    return not(cond1 and cond2)


def is_path(url):
    return not(not(urlparse(url).netloc) and url[0] != '/')


def new_resource_path(source, dir_path):
    new_name = true_name(source)
    new_path = make_path(dir_path, new_name)
    return new_path


def resource_filter(atr, parent_url, resources):
    first = [res for res in resources if is_parent_netloc(res[atr],
                                                          parent_url)]
    second = [res for res in first if is_path(res[atr])]
    return second


def get_resources(html_page, parent_url, dir_path):

    resource_tag = {'img': 'src', 'link': 'href', 'script': 'src'}
    for_downloading = []

    with open(html_page, 'r', encoding='utf-8') as hp:

        soup = bs(hp.read(), features="html.parser")

        for tag, atr in resource_tag.items():
            all_resources = soup.find_all(tag, attrs={atr: True})
            resource_list = resource_filter(atr, parent_url, all_resources)

            for res in resource_list:
                source = valid_link(res[atr], parent_url)
                res_path = new_resource_path(source, dir_path)
                res_description = dict([('tag', tag),
                                        ('source', source),
                                        ('res_path', res_path)])
                for_downloading.append(res_description)
                res[atr] = res_path

    with open(html_page, 'w') as hp:
        hp.write(soup.prettify())

    return for_downloading


def loading_res(res_description):
    tag = res_description['tag']
    source = res_description['source']
    res_path = res_description['res_path']
    if tag == 'img':
        data = request_http(source, bytes=True)
        writing(res_path, data, bytes=True)
    elif tag == 'link' or tag == 'script':
        data = request_http(source)
        writing(res_path, data)


def download_resources(resources_dict, writing_res=loading_res):
    if not resources_dict:
        logger.warning('На странице нет ресурсов, доступных для скачивания.')
        return
    res_count = len(resources_dict)
    with download_progress(res_count) as p:
        for res in resources_dict:
            try:
                writing_res(res)
            except CommonRequestsError:
                continue
            p.next()
