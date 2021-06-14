import re
import secrets
from typing import Tuple

from flask import Blueprint, current_app, request

from ggci.google_chat import GoogleChatError, send_message
from ggci.gitlab import MergeRequestEvent, InvalidFormat, UnsupportedEvent

_GITLAB_TOKEN_REGEX_PATTERN = 'GGCI-SECRET=(.*);GOOGLE-CHAT-URL=(.*)'
_GOOGLE_CHAT_REGEX_PATTERN = 'https://chat.googleapis.com/v1/spaces/.*'
_UNAUTHORIZED_RESPONSE = ('Unauthorized', 401)

bp = Blueprint('forwarder', __name__)


class IncorrectTokenFormat(Exception):
    pass


class Unauthorized(Exception):
    pass


def _parse_gitlab_token(gitlab_token: str) -> Tuple[str, str]:
    if not isinstance(gitlab_token, str):
        raise IncorrectTokenFormat()
    match = re.match(_GITLAB_TOKEN_REGEX_PATTERN, gitlab_token)
    if match is None:
        raise IncorrectTokenFormat()
    ggci_secret, google_chat_url = match.groups()
    return ggci_secret, google_chat_url


def _authorize(ggci_secret: str) -> None:
    if not secrets.compare_digest(
        ggci_secret, current_app.config['GGCI_SECRET']
    ):
        raise Unauthorized()


@bp.route('/', methods=['POST'])
def forward():

    try:
        ggci_secret, google_chat_url = _parse_gitlab_token(
            gitlab_token=request.headers.get('X-Gitlab-Token'),
        )
    except IncorrectTokenFormat:
        return _UNAUTHORIZED_RESPONSE

    try:
        _authorize(ggci_secret=ggci_secret)
    except Unauthorized:
        return _UNAUTHORIZED_RESPONSE

    if re.fullmatch(_GOOGLE_CHAT_REGEX_PATTERN, google_chat_url) is None:
        return (
            f'Google Chat URL does not match the following regex pattern:'
            f' {_GOOGLE_CHAT_REGEX_PATTERN}'
        ), 400

    try:
        mr_event = MergeRequestEvent.from_dict(request.json)
    except InvalidFormat as exc:
        return str(exc), 400
    except UnsupportedEvent as exc:
        return str(exc), 501

    try:
        send_message(url=google_chat_url, message=mr_event.create_message())
    except GoogleChatError as exc:
        return str(exc), 500

    return 'Success', 200
