import pytest
from page_loader.aux.print_message import user_friendly_message
from .fixtures.for_fixtures import FAKE_LINKS

r1 = 'The page not found, sorry.\n'
r2 = 'There is a browser error, try again later!\n'
r3 = "The directory not found or not " \
     "a directory, please try again!\n"
r4 = "The directory for resources: "
dir_name = FAKE_LINKS['dir_for_resources']


@pytest.mark.parametrize('message, response', [('not found dir', r3),
                                               ('404', r1),
                                               ('402', r2)])
def test_user_friendly_message1(capsys, message, response):
    user_friendly_message(message)
    out, err = capsys.readouterr()
    assert out == response


def test_user_friendly_message2(capsys):
    user_friendly_message('resource dir', dir_name)
    out, err = capsys.readouterr()
    assert out == r4 + dir_name + "\n"
