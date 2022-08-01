import os


FAKE_LINKS = {'normal_url': 'https://ru.hexlet.io/courses',
             'home': 'home_path',
             'dir_for_resources': 'ru-hexlet-io-courses_files',
             'new_html_dir': 'ru-hexlet-io-courses.html',
             'invalid_url1': 'htps://ru.hexlet.io/courses',
             'invalid_url2': 'https://ru.hexlet.ru/courses',
             'invalid_url3': '/ololo',
             'invalid_url4': 'http://some_domen.ru/courses',
             'error_dir1': 'ololo'}


def get_abs_path_fixture(fixt):
    return os.path.realpath(os.path.join('tests/fixtures', fixt))
    #return os.path.realpath(os.path.join('fixtures', fixt))


def fake_resources(*args):
    pass


def fake_downloading(path, *args):
    with open(path, 'x'):
        pass


def fake_writing(res, path, *args):
    res_path = os.path.join(path, res['res_path'])
    fake_downloading(res_path)


def fake_data(*args):
    file = get_abs_path_fixture('just_file.txt')
    with open(file, 'r') as f:
        fake_text = f.read()
    return fake_text
