import functools
import traceback
from flask import jsonify


http_exceptions = {
    "BadRequest": 400,
    "Unauthorized": 401,
    "Forbidden": 403,
    "NotFound": 404,
    "MethodNotAllowed": 405,
    "NotAcceptable": 406,
    "InternalServerError": 500,
    "BadGateway": 502,
    "ServiceUnavailable": 503,
    "GatewayTimeout": 504
}


def handles_exceptions(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            exception, description = traceback.format_exc().splitlines()[
                -1].split(": ")
            exit_code = http_exceptions[exception] \
                if exception in http_exceptions else 500
            return jsonify(exception, description), exit_code
    return wrapper
