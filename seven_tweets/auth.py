from flask import request, Response
from seven_tweets import config
import functools
import secrets


AUTH_TOKEN_NAME = 'X-Auth-Token'


def is_authorized(fn):
    """Verify user is authorized to execute query, otherwise decline."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        received_token = request.headers.get(AUTH_TOKEN_NAME)
        if received_token == config.auth_token:
            return fn(*args, **kwargs)
        else:
            return Response('access denied :-p :)', 401)
    return wrapper


def generate_token():
    """Generate acceptable token for application use."""
    return secrets.token_urlsafe(24)


if __name__ == "__main__":
    print("> hail all mighty user!")
    print("> here is your token, use it wisely :)\n{}"
          .format(generate_token()))

