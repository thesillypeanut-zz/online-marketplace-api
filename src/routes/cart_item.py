from flask import request

from src import constants
from src.helpers import handle_exception
from src.routes.decorators import json_response, token_required
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
@token_required
def list_cart_items(current_user):
    _ensure_current_user_has_carts(current_user.carts)

    if not request.args or not request.args.get('cart_id'):
        return 'Bad Request: Please include a "cart_id" in your route query.', 400

    cart_id = request.args['cart_id']

    if cart_id not in [str(cart.id) for cart in current_user.carts]:
        return f'Unauthorized: Cart with id "{cart_id}" is not associated with your account.', 401

    return cart_item_service.list_all({'cart_id': cart_id})


@json_response(200)
@token_required
def get_cart_item(current_user, cart_item_id):
    _ensure_current_user_has_carts(current_user.carts)

    cart_item = cart_item_service.get(cart_item_id)

    if cart_item['cart_id'] not in [cart.id for cart in current_user.carts]:
        return 'Unauthorized: You can only fetch a cart item added to your cart.', 401

    return cart_item


@json_response(201)
@token_required
def create_cart_item(current_user):
    return cart_item_service.create(request.json, current_user)


@json_response(200)
@token_required
def edit_cart_item(current_user, cart_item_id):
    _ensure_current_user_has_carts(current_user.carts)

    cart_item = cart_item_service.get(cart_item_id)

    if cart_item['cart_id'] not in [cart.id for cart in current_user.carts]:
        return 'Unauthorized: You can only edit a cart item in your cart.', 401

    return cart_item_service.update(cart_item_id, request.json)


@json_response(204)
@token_required
def delete_cart_item(current_user, cart_item_id):
    _ensure_current_user_has_carts(current_user.carts)

    cart_item = cart_item_service.get(cart_item_id)

    if cart_item['cart_id'] not in [cart.id for cart in current_user.carts]:
        return 'Unauthorized: You can only delete a cart item in your cart.', 401

    return cart_item_service.delete(cart_item_id)


def _ensure_current_user_has_carts(carts):
    if not carts:
        raise handle_exception(
            'Bad Request: Your account has no carts (and thus no cart items). POST a cart item to automatically '
            'create a cart for your account.', 400
        )
