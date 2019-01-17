from flask import request

from src import constants
from src.routes.decorators import json_response
from src.services import product_service

_PRODUCT_URL_PATH = f'{constants.BASE_URL_PATH}/products'

def add_routes(app):
    app.add_url_rule(
        rule=f'{_PRODUCT_URL_PATH}/',
        methods=['GET'],
        view_func=list_products,
        endpoint=list_products.__name__
    ),
    app.add_url_rule(
        rule=f'{_PRODUCT_URL_PATH}/<product_id>',
        methods=['GET'],
        view_func=get_product,
        endpoint=get_product.__name__
    ),
    app.add_url_rule(
        rule=f'{_PRODUCT_URL_PATH}/',
        methods=['POST'],
        view_func=create_product,
        endpoint=create_product.__name__
    ),
    app.add_url_rule(
        rule=f'{_PRODUCT_URL_PATH}/<product_id>',
        methods=['PUT'],
        view_func=edit_product,
        endpoint=edit_product.__name__
    ),
    app.add_url_rule(
        rule=f'{_PRODUCT_URL_PATH}/<product_id>',
        methods=['DELETE'],
        view_func=delete_product,
        endpoint=delete_product.__name__
    )


@json_response(200)
def list_products():
    return product_service.list_all(request.args)


@json_response(200)
def get_product(product_id):
    return product_service.get(product_id)


@json_response(201)
def create_product():
    return product_service.create(request.json)


@json_response(200)
def edit_product(product_id):
    return product_service.update(product_id, request.json)


@json_response(204)
def delete_product(product_id):
    return product_service.delete(product_id)
