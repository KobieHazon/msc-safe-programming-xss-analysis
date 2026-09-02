from __future__ import annotations

import base64
import re

import pytest
import XSSApp.app as xss_app


@pytest.fixture(autouse=True)
def configured_app():
    xss_app.messages.clear()
    xss_app.app.config.update(
        TESTING=True,
        SECRET_KEY=base64.b64encode(b"0123456789abcdef"),
    )
    yield
    xss_app.messages.clear()


def test_index_creates_a_session_and_csrf_token() -> None:
    response = xss_app.app.test_client().get("/")

    assert response.status_code == 200
    assert b'name="csrf_token"' in response.data
    assert "session=" in response.headers["Set-Cookie"]


def test_coursework_parser_behavior_is_preserved() -> None:
    client = xss_app.app.test_client()
    page = client.get("/").get_data(as_text=True)
    csrf_token = re.search(r'value="([^"]+)" name="csrf_token"', page)
    assert csrf_token is not None

    response = client.post(
        "/request",
        data={
            "name": "Local Tester",
            "phone_number": "+12025550123",
            "email": "local-user",
            "subject": "Local exercise",
            "message": "<iframe src=javascript:alert(1)>",
            "csrf_token": csrf_token.group(1),
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"<iframe src=javascript:alert(1)>" in response.data
    assert b"Local Tester (Weak)" in response.data


def test_on_event_attributes_are_rejected() -> None:
    with pytest.raises(ValueError, match="on attribute"):
        xss_app.validation_utilities.validate_message('<img src="x" onerror="alert(1)">')
