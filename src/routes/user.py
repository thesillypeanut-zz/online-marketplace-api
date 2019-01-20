from flask import request

from src import constants
from src.routes.decorators import json_response, token_required
from src.services import user_service

_USER_URL_PATH = f'{constants.BASE_URL_PATH}/users'


def add_routes(app):
    app.add_url_rule(
        rule=f'{_USER_URL_PATH}/',
        methods=['GET'],
        view_func=list_users,
        endpoint=list_users.__name__
    ),
    app.add_url_rule(
        rule=f'{_USER_URL_PATH}/<user_id>',
        methods=['GET'],
        view_func=get_user,
        endpoint=get_user.__name__
    ),
    app.add_url_rule(
        rule=f'{_USER_URL_PATH}/',
        methods=['POST'],
        view_func=create_user,
        endpoint=create_user.__name__
    ),
    app.add_url_rule(
        rule=f'{_USER_URL_PATH}/<user_id>',
        methods=['PUT'],
        view_func=edit_user,
        endpoint=edit_user.__name__
    ),
    app.add_url_rule(
        rule=f'{_USER_URL_PATH}/<user_id>',
        methods=['DELETE'],
        view_func=delete_user,
        endpoint=delete_user.__name__
    ),
    app.add_url_rule(
        rule=f'{_USER_URL_PATH}/login',
        methods=['GET'],
        view_func=login_user,
        endpoint=login_user.__name__
    )


@json_response(200)
@token_required
def list_users(current_user):
    return user_service.list_all(request.args)


@json_response(200)
@token_required
def get_user(current_user, user_id):
    return user_service.get(user_id)


@json_response(201)
def create_user():
    return user_service.create(request.json)


@json_response(200)
@token_required
def edit_user(current_user, user_id):
    if str(current_user.id) != user_id:
        return 'Unauthorized: You can only edit the user info for your account.', 401

    return user_service.update(user_id, request.json)


@json_response(204)
@token_required
def delete_user(current_user, user_id):
    if str(current_user.id) != user_id:
        return 'Unauthorized: You can only delete your account.', 401

    return user_service.delete(user_id)


@json_response(200)
def login_user():
    return user_service.login(request.authorization)
