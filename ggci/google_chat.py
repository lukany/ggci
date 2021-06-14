import logging

import requests

from ggci.commons import Message

_LOGGER = logging.getLogger(__name__)


def send_message(url: str, message: Message) -> None:

    _LOGGER.info('Sending message...')
    _LOGGER.debug('Message: %s', message)

    if message.thread_key is not None:
        url += f'&threadKey=GGCI_{message.thread_key}'

    requests.post(url=url, json={'text': message.text})
