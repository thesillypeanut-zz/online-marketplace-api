from src import constants

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
        rule=f'{_CART_URL_PATH}/',
        methods=['POST'],
        view_func=create_cart,
        endpoint=create_cart.__name__
    ),
    app.add_url_rule(
        rule=f'{_CART_URL_PATH}/<cart_id>',
        methods=['PUT'],
        view_func=edit_cart,
        endpoint=edit_cart.__name__
    ),
    app.add_url_rule(
        rule=f'{_CART_URL_PATH}/<cart_id>',
        methods=['DELETE'],
        view_func=delete_cart,
        endpoint=delete_cart.__name__
    )


def list_carts():
    return "Hello"


def get_cart(cart_id):
    pass


def create_cart():
    pass


def edit_cart(cart_id):
    pass


def delete_cart(cart_id):
    pass
