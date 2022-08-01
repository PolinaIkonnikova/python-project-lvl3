import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Page Loader')
    parser.add_argument('--output', type=str, default="home_path",
                        help='your home path')
    parser.add_argument('url', type=str, default="no_page",
                        help='path of loaded file')
    args = parser.parse_args()
    return args.url, args.output
