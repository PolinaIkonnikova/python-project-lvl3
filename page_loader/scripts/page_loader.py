#!/usr/bin/env python

import sys
from page_loader.arg_parser import create_parser
from page_loader.page_output import download_page
from page_loader.resources_output import download_resources, get_resources
from page_loader.work_with_files import prepare_dir, valid_dir
from page_loader.aux.logs_config import success_logger
from page_loader.aux.custom_exceptions import CommonPageLoaderException, NoResourcesException


logger = success_logger(__name__)


def downloading(url, output_path):
    try:
        output_path = valid_dir(output_path)
        page_path = download_page(url, output_path)
    except CommonPageLoaderException:
        sys.exit(1)
    else:
        try:
            logger.debug('Cтраница скачалась, переходим к ресурсам')
            new_dir = prepare_dir(url, output_path)
            logger.debug(f'Директория для ресурсов {new_dir}')
            resources = get_resources(page_path, url, new_dir)
            download_resources(resources, output_path)
            #можно сделать счетчик, сколько ресурсов загружено, сколько ошибочно
            logger.info(f'Cтраница успешно сохранена {page_path}')
            sys.exit(0)
        except NoResourcesException:
            sys.exit(0)
        except FileExistsError:
            sys.exit(2)


def main(get_args=create_parser):
    url, output_path = get_args()
    downloading(url, output_path)


if __name__ == '__main__':
    main()
