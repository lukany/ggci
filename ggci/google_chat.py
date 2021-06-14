import logging

import requests
import tenacity

from ggci.commons import Message

_LOGGER = logging.getLogger(__name__)


class GoogleChatError(Exception):
    def __init__(self, error):

        if isinstance(error, tenacity.Future):
            # Tenacity initiates `retry_error_cls` with tenacity.Future.
            # containing more information along with the exception itself
            error = error.exception()

        super().__init__(error)


@tenacity.retry(
    retry=tenacity.retry_if_exception_type(requests.exceptions.HTTPError),
    stop=tenacity.stop_after_attempt(5),
    wait=tenacity.wait.wait_random(min=0.05, max=0.2),
    retry_error_cls=GoogleChatError,
)
def send_message(url: str, message: Message) -> None:

    _LOGGER.info('Sending message...')
    _LOGGER.debug('Message: %s', message)

    if message.thread_key is not None:
        url += f'&threadKey=GGCI_{message.thread_key}'

    response = requests.post(url=url, json={'text': message.text})
    response.raise_for_status()
