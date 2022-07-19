import for_http
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from .work_with_files import true_name, make_path
from .progress_bar import download_progress
from .logs.logs_config import make_logger


logger = make_logger()


def is_parent_netloc(url, parent_url):
    return not(bool(urlparse(url).netloc) is True and urlparse(url).netloc != urlparse(parent_url).netloc)


def new_resource_path(source, dir_path):
    new_name = true_name(source)
    new_path = make_path(dir_path, new_name)
    return new_path


def resource_filter(atr, parent_url, resources):
    return [res for res in resources if is_parent_netloc(res[atr], parent_url)]


def get_resources(html_page, parent_url, dir_path):

    resource_tag = {'img': 'src', 'link': 'href', 'script': 'src'}
    for_downloading = {}

    with open(html_page, 'r', encoding='utf-8') as hp:

        soup = bs(hp.read(), features="html.parser")

        for tag, atr in resource_tag.items():
            all_resources = soup.find_all(tag, attrs={atr: True})
            resource_list = resource_filter(atr, parent_url, all_resources)

            for res in resource_list:
                source = for_http.valid_link(res[atr], parent_url)
                res_path = new_resource_path(source, dir_path)
                res_description = dict([('tag', tag),
                                        ('source', source),
                                        ('res_path', res_path)])
                for_downloading.update(res_description)
                res[atr] = res_path

    with open(html_page, 'w') as hp:
        hp.write(soup.prettify())

    return for_downloading


def loading_res(res_description):
    tag = res_description['tag']
    source = res_description['source']
    res_path = res_description['source']
    try:
        data = for_http.request_http(source)
    except Exception as e:
        raise e

    if tag == 'img':
        for_http.writing(res_path, data, bytes=True)
    else:
        for_http.writing(res_path, data)


def download_resources(resources_dict):
    res_count = len(resources_dict)
    with download_progress(res_count) as p:
        for res in resources_dict:
            loading_res(res)
            p.next()




