import pytest


some_string = 'olololo.html'
url_error_schema = ''
normal_img = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZmNcheLzMthy3Q04NhmZcdewmZG6vq1NjJg&usqp=CAU'
fake_image = 'htps://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZmNcheLzMthy3Q04NhmZcdewmZG6vq1NjJg&usqp=CAU'

normal_url_hexlet = 'https://ru.hexlet.io/courses'
dir_name_hexlet = 'ru-hexlet-io-courses_files'
html_name_hexlet = 'ru-hexlet-io-courses.html'

@pytest.fixture
def fake_resources(path_page, url, name_new_dir):
    pass


@pytest.fixture
def fake_downloading(path, url):
    with open(path, 'x'):
        pass

