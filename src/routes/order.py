from flask import request

from src import constants
from src.routes.decorators import json_response, token_required
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
@token_required
def list_orders(current_user):
    if not current_user.carts or not any([cart.order for cart in current_user.carts]):
        return []

    cart_ids = [cart.id for cart in current_user.carts if cart.order]
    return order_service.list_all(cart_ids)


@json_response(200)
@token_required
def get_order(current_user, order_id):
    if not current_user.carts or not any([cart.order for cart in current_user.carts]):
        return 'Bad Request: Your account has no orders to query.', 400

    if order_id not in [str(cart.order[0].id) for cart in current_user.carts if cart.order]:
        return 'Unauthorized: You can only fetch orders created from your account.', 401

    return order_service.get(order_id)


@json_response(201)
@token_required
def create_order(current_user):
    return order_service.create(request.json, current_user)
