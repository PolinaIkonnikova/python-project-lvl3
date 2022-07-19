import requests
from .for_http import request_http, writing
from .work_with_files import true_name, make_path
from .logs.logs_config import make_logger

# fixt = '/home/ulitka/python-project-lvl3/page_loader/tests/fixtures/before1.html'
# url = 'https://ru.hexlet.io/courses'
# home_path = "/home/ulitka/python-project-lvl3/page_loader"
# #print(get_resources(fixt, url, home_path), sep='\n')
# print(get_resources(fixt, url, home_path))


logger = make_logger()


def download_page(url,
                  output_path,
                  get_content=request_http
                  ):
    try:
        html_path = make_path(output_path, true_name(url))
        content = get_content(url)
        new_html = writing(url, html_path, content)
    except requests.RequestException as re:
        raise re
    except PermissionError as pe:
        raise pe
    else:
        return new_html



    # try:
    #     r = requests.get(url)
    #     return r.status_code
    #
    #     #logger.warning(f'Something went wrong, a response code is {r.status_code}')
    # except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
    #     raise requests.RequestException(f'The url {url} is not valid')
    # except requests.exceptions.ConnectionError:
    #     code = requests.get(url).status_code
    #     raise requests.RequestException(f'Problems with connecting for {url}. Status code is {code}')
    # except requests.RequestException:
    #     logger.error('Something went wrong for downloading')

