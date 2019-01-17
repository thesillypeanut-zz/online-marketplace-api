from flask import request

from src import constants
from src.routes.decorators import json_response
from src.services import order_service

_ORDER_URL_PATH = f'{constants.BASE_URL_PATH}/orders'

def add_routes(app):
    app.add_url_rule(
        rule=f'{_ORDER_URL_PATH}/',
        methods=['GET'],
        view_func=list_orders,
        endpoint=list_orders.__name__
    ),
    app.add_url_rule(
        rule=f'{_ORDER_URL_PATH}/<order_id>',
        methods=['GET'],
        view_func=get_order,
        endpoint=get_order.__name__
    ),
    app.add_url_rule(
        rule=f'{_ORDER_URL_PATH}/',
        methods=['POST'],
        view_func=create_order,
        endpoint=create_order.__name__
    )


@json_response(200)
def list_orders():
    return order_service.list_all()


@json_response(200)
def get_order(order_id):
    return order_service.get(order_id)


@json_response(201)
def create_order():
    return order_service.create(request.json)
