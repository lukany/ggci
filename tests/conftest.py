from typing import Any, Dict, Iterator

import pytest
from flask.testing import FlaskClient

from ggci import create_app, Config, load_yaml_config
from ggci.gitlab import MergeRequestEvent

_CONFIG = load_yaml_config('example_config.yaml')


def _create_payload():
    return {
        'event_type': 'merge_request',
        'user': {'id': 1, 'name': 'Chuck Norris'},
        'object_attributes': {
            'id': 42,
            'iid': 42,
            'assignee_ids': [1],
            'description': (
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit,'
                ' sed do eiusmod tempor incididunt ut labore et dolore'
                ' magna aliqua. Ut enim ad minim veniam, quis nostrud'
                ' exercitation ullamco laboris nisi ut aliquip ex ea'
                ' commodo consequat.'
                ' Duis aute irure dolor in reprehenderit in voluptate'
                ' velit esse cillum dolore eu fugiat nulla pariatur.'
                ' Excepteur sint occaecat cupidatat non proident, sunt in'
                ' culpa qui officia deserunt mollit anim id est laborum.'
            ),
            'action': 'open',
            'url': 'https://www.gitlab.com/lukany/ggci',
            'title': 'Improve the world',
        },
        'changes': {},
    }


def _create_mr_event(payload: Dict[str, Any]) -> MergeRequestEvent:
    return MergeRequestEvent.from_dict(payload)


@pytest.fixture
def headers() -> Dict[str, Any]:
    return {'X-GitLab-Token': _CONFIG['GGCI_GITLAB_TOKEN']}


@pytest.fixture(scope='session')
def client() -> Iterator[FlaskClient]:
    config = Config(
        gitlab_token=_CONFIG['GGCI_GITLAB_TOKEN'],
        google_chat_url=_CONFIG['GGCI_GOOGLE_CHAT_URL'],
        user_mappings=_CONFIG['GGCI_USER_MAPPINGS'],
    )
    app = create_app(config)
    app.testing = True
    yield app.test_client()


@pytest.fixture(scope='function')
def payload_mr_open() -> MergeRequestEvent:
    payload = _create_payload()
    payload['object_attributes']['action'] = 'open'
    yield payload


@pytest.fixture(scope='function')
def payload_mr_update() -> MergeRequestEvent:
    payload = _create_payload()
    payload['object_attributes']['action'] = 'update'
    payload['changes']['assignees'] = {
        'previous': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}],
        'current': [{'id': 3, 'name': 'Carl'}, {'id': 4, 'name': 'Dick'}],
    }
    yield payload


@pytest.fixture(scope='function')
def payload_mr_approved() -> MergeRequestEvent:
    payload = _create_payload()
    payload['object_attributes']['action'] = 'approved'
    yield payload


@pytest.fixture(scope='function')
def payload_mr_merge() -> MergeRequestEvent:
    payload = _create_payload()
    payload['object_attributes']['action'] = 'merge'
    yield payload


@pytest.fixture(scope='function')
def payload_mr_close() -> MergeRequestEvent:
    payload = _create_payload()
    payload['object_attributes']['action'] = 'close'
    yield payload


@pytest.fixture(scope='function')
def payload_mr_reopen() -> MergeRequestEvent:
    payload = _create_payload()
    payload['object_attributes']['action'] = 'reopen'
    yield payload
