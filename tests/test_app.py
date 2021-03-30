from typing import Any, Dict

import pytest
from flask.testing import FlaskClient


def test_unauthorized(client):
    assert client.post().status_code == 401


def test_empty(client: FlaskClient, headers):
    with pytest.raises(Exception):
        client.post(headers=headers, json={})


@pytest.mark.live_google_chat
def test_open(client: FlaskClient, headers, payload_mr_open):
    client.post(headers=headers, json=payload_mr_open)


@pytest.mark.live_google_chat
def test_update(client: FlaskClient, headers, payload_mr_update):
    client.post(headers=headers, json=payload_mr_update)


@pytest.mark.live_google_chat
def test_approved(client: FlaskClient, headers, payload_mr_approved):
    client.post(headers=headers, json=payload_mr_approved)


@pytest.mark.live_google_chat
def test_merge(client: FlaskClient, headers, payload_mr_merge):
    client.post(headers=headers, json=payload_mr_merge)
