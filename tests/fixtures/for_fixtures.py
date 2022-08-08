import os


FAKE_LINKS = {'normal_url': 'https://ru.hexlet.io/courses',
              'home': 'home_path',
              'dir_for_resources': 'ru-hexlet-io-courses_files',
              'new_html_name': 'ru-hexlet-io-courses.html',
              'invalid_url1': 'htps://ru.hexlet.io/courses',
              'invalid_url2': 'https://ru.hexlet.ru/courses',
              'invalid_url3': '/ololo',
              'invalid_url4': 'http://some_domen.ru/courses',
              'error_dir1': 'ololo'}


def get_path_fixture(fixt):
    path = os.getcwd()
    if path.split('/')[-1] == 'tests':
        return os.path.join('fixtures', fixt)
    return os.path.join('tests/fixtures', fixt)
