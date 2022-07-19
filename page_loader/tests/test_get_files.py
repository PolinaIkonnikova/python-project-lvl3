import os
import tempfile
import pytest
from page_loader.work_with_files import prepare_dir, prepare_html, valid_path
from page_loader.scripts.page_loader import downloading


fake_url = 'htps:/olololo.html'
fake_path = 'olololo.html'
# url_error_schema = ''
# normal_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZmNcheLzMthy3Q04NhmZcdewmZG6vq1NjJg&usqp=CAU'
# fake_image = 'htps://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZmNcheLzMthy3Q04NhmZcdewmZG6vq1NjJg&usqp=CAU'
url = 'https://ru.hexlet.io/courses'
dir_name = 'ru-hexlet-io-courses_files'
html_name_hexlet = 'ru-hexlet-io-courses.html'


def test_valid_output_path():
    path = valid_path('home_path')
    assert path == os.getcwd()

    with pytest.raises(NotADirectoryError):
        valid_path(fake_path)


# @pytest.mark.skip
def test_prepare_dir1():
    with tempfile.TemporaryDirectory() as d:
        dir_pass = prepare_dir(url, d)
        assert os.path.exists(os.path.join(d, dir_name))
        assert dir_pass == os.path.join(d, dir_name)


def test_prepare_dir2():
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises(FileExistsError):
            os.mkdir(dir_name)
            prepare_dir(url, d)


def test_prepare_dir3():
    with pytest.raises(FileNotFoundError):
        prepare_dir(url, fake_path)


def test_downloading_with_fake_files():  # использовать много фикстур и вариантов ошибочных страниц
    try:
        downloading(url, fake_url)
    except SystemExit:
        assert 1


# @pytest.mark.skip
def test_prepare_html():
    with tempfile.TemporaryDirectory() as d:
        html_path = prepare_html(url, d)
        assert os.path.exists(os.path.join(d, html_name_hexlet))
        assert html_path == os.path.join(d, html_name_hexlet)
