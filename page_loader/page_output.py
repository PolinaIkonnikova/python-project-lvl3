import requests
from .for_http import request_http
from .work_with_files import true_name, make_path, valid_dir, writing
from .aux.logs_config import mistakes_logging
from .aux.custom_exceptions import CommonPageLoaderException, CommonRequestsError


# fixt = '/home/ulitka/python-project-lvl3/page_loader/tests/fixtures/before1.html'
# url = 'https://ru.hexlet.io/courses'
# home_path = "/home/ulitka/python-project-lvl3/page_loader"
# #print(get_resources(fixt, url, home_path), sep='\n')
# print(get_resources(fixt, url, home_path))


def download_page(url,
                  output_path,
                  get_content=request_http
                  ):
    try:
        #valid_url(url)
        new_html = make_path(output_path, true_name(url))
        content = get_content(url)
        writing(new_html, content)
        return new_html
    except CommonRequestsError as e:
        error = e.error
        url = e.url
        code = e.code
        #mistakes_logging(error, 7, url, code)
        raise CommonPageLoaderException
    except requests.RequestException as e:
        print(e)
    #     mistakes_logging(e, 7, url)
        raise CommonPageLoaderException


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
