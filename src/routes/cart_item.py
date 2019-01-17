from flask import request

from src import constants
from src.routes.decorators import json_response
from src.services import cart_item_service

_CART_ITEM_URL_PATH = f'{constants.BASE_URL_PATH}/cart-items'

def add_routes(app):
    app.add_url_rule(
        rule=f'{_CART_ITEM_URL_PATH}/',
        methods=['GET'],
        view_func=list_cart_items,
        endpoint=list_cart_items.__name__
    ),
    app.add_url_rule(
        rule=f'{_CART_ITEM_URL_PATH}/<cart_item_id>',
        methods=['GET'],
        view_func=get_cart_item,
        endpoint=get_cart_item.__name__
    ),
    app.add_url_rule(
        rule=f'{_CART_ITEM_URL_PATH}/',
        methods=['POST'],
        view_func=create_cart_item,
        endpoint=create_cart_item.__name__
    ),
    app.add_url_rule(
        rule=f'{_CART_ITEM_URL_PATH}/<cart_item_id>',
        methods=['PUT'],
        view_func=edit_cart_item,
        endpoint=edit_cart_item.__name__
    ),
    app.add_url_rule(
        rule=f'{_CART_ITEM_URL_PATH}/<cart_item_id>',
        methods=['DELETE'],
        view_func=delete_cart_item,
        endpoint=delete_cart_item.__name__
    )


@json_response(200)
def list_cart_items():
    return cart_item_service.list_all(request.args)


@json_response(200)
def get_cart_item(cart_item_id):
    return cart_item_service.get(cart_item_id)


@json_response(201)
def create_cart_item():
    return cart_item_service.create(request.json)


@json_response(200)
def edit_cart_item(cart_item_id):
    return cart_item_service.update(cart_item_id, request.json)


@json_response(204)
def delete_cart_item(cart_item_id):
    return cart_item_service.delete(cart_item_id)
