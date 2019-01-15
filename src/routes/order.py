from src import constants

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
    ),
    app.add_url_rule(
        rule=f'{_ORDER_URL_PATH}/<order_id>',
        methods=['DELETE'],
        view_func=delete_order,
        endpoint=delete_order.__name__
    )


def list_orders():
    pass


def get_order(order_id):
    pass


def create_order():
    pass


def delete_order(order_id):
    pass
