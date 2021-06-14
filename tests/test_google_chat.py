import flexmock
import pytest
import requests

from ggci.commons import Message
from ggci.google_chat import GoogleChatError, send_message


def mocked_post(*args, **kwargs):
    raise requests.exceptions.HTTPError()


def test_send_message():
    flexmock(requests, post=mocked_post)
    with pytest.raises(GoogleChatError):
        send_message(
            url='http://www.github.com',
            message=Message(text='testing'),
        )
