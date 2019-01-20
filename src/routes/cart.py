from src import constants
from src.routes.decorators import json_response, token_required
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
@token_required
def list_carts(current_user):
    return cart_service.list_all({'customer_id': current_user.id})


@json_response(200)
@token_required
def get_cart(current_user, cart_id):
    if not current_user.carts:
        return 'Unauthorized: You can only fetch your own carts.', 401

    if cart_id not in [str(cart.id) for cart in current_user.carts]:
        return 'Unauthorized: You can only fetch your own carts.', 401

    return cart_service.get(cart_id)


@json_response(204)
@token_required
def delete_cart(current_user, cart_id):
    cart = cart_service.get(cart_id)

    if cart['customer_id'] != current_user.id:
        return 'Unauthorized: You can only delete your own carts.', 401

    return cart_service.delete(cart_id)
