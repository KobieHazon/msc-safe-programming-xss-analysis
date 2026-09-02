from __future__ import annotations

import base64

import pytest
from flask import Flask
from flask.sessions import SecureCookieSessionInterface

from solution.flask_cookie_generator import decode_logged_secret, elevate_session_cookie


def test_elevate_session_cookie_preserves_data_and_sets_admin() -> None:
    secret_key = base64.b64encode(b"0123456789abcdef")
    application = Flask(__name__)
    application.secret_key = secret_key
    serializer = SecureCookieSessionInterface().get_signing_serializer(application)
    assert serializer is not None

    original = serializer.dumps({"csrf_token": "local-token", "is_admin": False})
    logged_secret = base64.b64encode(secret_key).decode("ascii")
    elevated = elevate_session_cookie(original, logged_secret)

    decoded = serializer.loads(elevated)
    assert decoded == {"csrf_token": "local-token", "is_admin": True}


@pytest.mark.parametrize("value", ["", "not base64", "***"])
def test_decode_logged_secret_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValueError):
        decode_logged_secret(value)
