from src import constants

_PRODUCT_URL_PATH = f'{constants.BASE_URL_PATH}/products'

def add_routes(app):
    app.add_url_rule(
        rule=f'{_PRODUCT_URL_PATH}/',
        methods=['GET'],
        view_func=list_products,
        endpoint=list_products.__name__
    ),
    app.add_url_rule(
        rule=f'{_PRODUCT_URL_PATH}/available',
        methods=['GET'],
        view_func=list_available_products,
        endpoint=list_available_products.__name__
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
        methods=['DELETE'],
        view_func=delete_product,
        endpoint=delete_product.__name__
    )


def list_available_products():
    pass


def list_products():
    pass


def get_product(product_id):
    pass


def create_product():
    pass


def delete_product(product_id):
    pass
