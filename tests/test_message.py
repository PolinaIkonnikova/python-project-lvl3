import pytest
from page_loader.aux.print_message import user_friendly_message
from .fixtures.for_fixtures import FAKE_LINKS

MESSAGE1 = 'The page not found, sorry.\n'
MESSAGE2 = 'There is a browser error, try again later!\n'
MESSAGE3 = "The directory not found or not " \
           "a directory, please try again!\n"
MESSAGE4 = "The directory for resources: "
DIR_NAME = FAKE_LINKS['dir_for_resources']


@pytest.mark.parametrize('message, response', [('not found dir', MESSAGE3),
                                               ('404', MESSAGE1),
                                               ('402', MESSAGE2)])
def test_user_friendly_message1(capsys, message, response):
    user_friendly_message(message)
    out, err = capsys.readouterr()
    assert out == response


def test_user_friendly_message2(capsys):
    user_friendly_message('resource dir', DIR_NAME)
    out, err = capsys.readouterr()
    assert out == MESSAGE4 + DIR_NAME + "\n"
