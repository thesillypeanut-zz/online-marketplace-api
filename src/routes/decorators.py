import functools
from flask import make_response, jsonify


def json_response(status_code):

    def outer_wrapper(func):

        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            payload = func(*args, **kwargs)

            if isinstance(payload, dict) or isinstance(payload, list):
                return make_response(jsonify(payload), status_code)
            return make_response(payload)

        return inner_wrapper

    return outer_wrapper
