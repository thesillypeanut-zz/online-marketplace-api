from flask import request

from src import constants
from src.routes.decorators import json_response
from src.services import cart_service

_CART_URL_PATH = f'{constants.BASE_URL_PATH}/carts'

def add_routes(app):
    app.add_url_rule(
        rule=f'{_CART_URL_PATH}/',
        methods=['GET'],
        view_func=list_carts,
        endpoint=list_carts.__name__
    ),
    app.add_url_rule(
        rule=f'{_CART_URL_PATH}/<cart_id>',
        methods=['GET'],
        view_func=get_cart,
        endpoint=get_cart.__name__
    ),
    app.add_url_rule(
        rule=f'{_CART_URL_PATH}/<cart_id>',
        methods=['DELETE'],
        view_func=delete_cart,
        endpoint=delete_cart.__name__
    )


@json_response(200)
def list_carts():
    return cart_service.list_all(request.args)


@json_response(200)
def get_cart(cart_id):
    return cart_service.get(cart_id)


@json_response(204)
def delete_cart(cart_id):
    return cart_service.delete(cart_id)
