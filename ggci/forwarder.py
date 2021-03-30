from flask import Blueprint, current_app, request

from ggci.google_chat import send_message
from ggci.gitlab import MergeRequestEvent, UnsupportedEvent

bp = Blueprint('forwarder', __name__)


def _get_gitlab_token():
    return current_app.config['GGCI_GITLAB_TOKEN']


@bp.route('/', methods=['POST'])
def forward():

    if request.headers.get('X-Gitlab-Token') != _get_gitlab_token():
        return '', 401

    try:
        mr_event = MergeRequestEvent.from_dict(request.json)
    except UnsupportedEvent as exc:
        return exc, 501

    send_message(message=mr_event.create_message())

    return 'Success', 200
