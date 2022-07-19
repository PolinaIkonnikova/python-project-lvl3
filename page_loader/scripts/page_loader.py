#!/usr/bin/env python
import sys
import argparse
import requests
from page_loader.page_output import download_page
from page_loader.resources_output import download_resources, get_resources
from page_loader.work_with_files import prepare_dir
from page_loader.logs.logs_config import make_logger


logger = make_logger()


def downloading(url, output_path):
    try:
        page_path = download_page(url, output_path)
        new_dir = prepare_dir(url, output_path)
    except (FileNotFoundError, NotADirectoryError):
        logger.error("This directory doesn't exist. Please change another dir!")
        sys.exit(1)
    except PermissionError:
        logger.error("You doesn't have access rights, please choose another dir")
        sys.exit(1)
    except FileExistsError:
        logger.error("The directory already exist")
        sys.exit(1)
    except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
        logger.error('HTTP error occured. Seems this is not a page!')
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        logger.error('Connection failed, try again!')
        sys.exit(1)
    except requests.RequestException:
        logger.error('Something went wrong for downloading')
        sys.exit(1)

    else:
        resources = get_resources(page_path, url, new_dir)
        download_resources(resources) #можно сделать счетчик, сколько ресурсов загружено, сколько ошибочно
        logger.info(f'the page was loaded as {page_path}')


def main():
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('--output', type=str, default="home_path",
                        help='your home path')
    parser.add_argument('url', type=str, help='path of loaded file')
    args = parser.parse_args()
    downloading(args.url, args.output)


if __name__ == '__main__':
    main()
