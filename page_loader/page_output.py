from .for_http import request_http
from .work_with_files import true_name, make_path, writing
from .aux.logs_config import mistake_logger
from .aux.custom_exceptions import CommonPageLoaderException
from .aux.custom_exceptions import CommonRequestsError
from page_loader.resources_output import download_resources, get_resources
from page_loader.work_with_files import prepare_dir, valid_dir


logger = mistake_logger(__name__)


def download_page(url,
                  output_path,
                  get_content=request_http
                  ):
    try:
        new_html = make_path(output_path, true_name(url))
        content = get_content(url)
        writing(new_html, content)
        return new_html
    except CommonRequestsError as e:
        logger.warning(e.error)
        raise


def download(url, output_path):
    try:
        output_path = valid_dir(output_path)
        page_path = download_page(url, output_path)
        logger.debug('Cтраница скачалась, переходим к ресурсам')
        dir_name, dir_path = prepare_dir(url, output_path)
        logger.debug(f'Директория для ресурсов {dir_path}')
        resources = get_resources(page_path, url, dir_name)
        download_resources(resources, output_path)
        return page_path
    except CommonPageLoaderException:
        raise
    except FileExistsError:
        raise
