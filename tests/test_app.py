from typing import Any, Dict

import pytest
from flask.testing import FlaskClient


def test_unauthorized(client):
    assert client.post().status_code == 401


def test_empty(client: FlaskClient, headers):
    response = client.post(headers=headers, json={})
    assert response.status_code == 400


@pytest.mark.live_google_chat
def test_open(client: FlaskClient, headers, payload_mr_open):
    response = client.post(headers=headers, json=payload_mr_open)
    assert response.status_code == 200


@pytest.mark.live_google_chat
def test_update(client: FlaskClient, headers, payload_mr_update):
    response = client.post(headers=headers, json=payload_mr_update)
    assert response.status_code == 200


@pytest.mark.live_google_chat
def test_approved(client: FlaskClient, headers, payload_mr_approved):
    response = client.post(headers=headers, json=payload_mr_approved)
    assert response.status_code == 200


@pytest.mark.live_google_chat
def test_merge(client: FlaskClient, headers, payload_mr_merge):
    response = client.post(headers=headers, json=payload_mr_merge)
    assert response.status_code == 200
