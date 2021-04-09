from typing import Any, Dict

import pytest

from ggci.gitlab import MergeRequestEvent, UnsupportedEvent
from ggci import commons


def test_open(payload_mr_open: Dict[str, Any], monkeypatch):
    mr_event = MergeRequestEvent.from_dict(payload_mr_open)
    monkeypatch.setattr(commons, '_get_google_chat_id', lambda _: 100042)
    message = mr_event.create_message()

    assert '*Opened*' in message.text
    assert 'by Chuck Norris' in message.text
    assert '*Assignees:* <users/100042>' in message.text


def test_update(payload_mr_update: Dict[str, Any], monkeypatch):
    mr_event = MergeRequestEvent.from_dict(payload_mr_update)
    user_mappings = {
        1: 1001,
        4: 1004,
    }
    monkeypatch.setattr(commons, '_get_google_chat_id', user_mappings.get)
    message = mr_event.create_message()

    assert (
        '<https://www.gitlab.com/lukany/ggci|!42> *reassigned*' in message.text
    )
    assert 'by Chuck Norris' in message.text
    assert '\tPrevious assignees: Alice, Bob' in message.text
    assert '\tCurrent assignees: Carl, <users/1004>' in message.text


def test_approved(payload_mr_approved: Dict[str, Any]):
    mr_event = MergeRequestEvent.from_dict(payload_mr_approved)
    message = mr_event.create_message()
    assert message.text == (
        '<https://www.gitlab.com/lukany/ggci|!42> *approved* by Chuck Norris.'
    )


def test_merge(payload_mr_merge: Dict[str, Any]):
    mr_event = MergeRequestEvent.from_dict(payload_mr_merge)
    message = mr_event.create_message()
    assert (
        message.text
        == '<https://www.gitlab.com/lukany/ggci|!42> *merged* by Chuck Norris.'
    )


def test_no_action(payload_mr_open: Dict[str, Any]):
    payload_without_action = payload_mr_open
    del payload_without_action['object_attributes']['action']
    with pytest.raises(UnsupportedEvent):
        MergeRequestEvent.from_dict(payload_without_action)


def test_invalid_action(payload_mr_open: Dict[str, Any]):
    payload_invalid_action = payload_mr_open
    payload_invalid_action['object_attributes']['action'] = 'shredded'
    with pytest.raises(UnsupportedEvent):
        MergeRequestEvent.from_dict(payload_invalid_action)
