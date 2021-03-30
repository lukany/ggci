import logging
from typing import Optional

import requests
from flask import current_app


from ggci.commons import Message

_LOGGER = logging.getLogger(__name__)


def _get_google_chat_url() -> Optional[str]:
    return current_app.config.get('GGCI_GOOGLE_CHAT_URL')


def send_message(message: Message) -> None:

    url = _get_google_chat_url()

    if not isinstance(url, str):
        raise TypeError(f'Google Chat URL must be str, got: {type(url)}')
    if not url:
        raise ValueError('Google Chat URL must not be empty')

    _LOGGER.info('Sending message...')
    _LOGGER.debug('Message: %s', message)

    if message.thread_key is not None:
        url += f'&threadKey=GGCI_{message.thread_key}'

    requests.post(url=url, json={'text': message.text})
