import jwt
from functools import wraps
from flask import make_response, jsonify, request

from src.config import Config
from src.models import User


def json_response(status_code):

    def outer_wrapper(func):

        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            payload = func(*args, **kwargs)

            if isinstance(payload, dict) or isinstance(payload, list):
                return make_response(jsonify(payload), status_code)
            return make_response(payload)

        return inner_wrapper

    return outer_wrapper


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return 'Unauthorized: Token is missing!', 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return 'Unauthorized: Token is invalid!', 401

        if not current_user:
            return 'Unauthorized: Token is invalid!', 401

        return f(current_user, *args, **kwargs)

    return decorated
