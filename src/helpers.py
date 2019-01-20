import uuid
from flask import make_response
from werkzeug import exceptions


def generate_uuid():
    return uuid.uuid4()


def validate_cart_item_quantity_is_not_more_than_product_inventory(product_inventory, item_quantity, product_id):
    if product_inventory < item_quantity:
        raise handle_exception(
            f'Bad Request: Cannot add product with id "{product_id}" of quantity "{item_quantity}". '
            f'The associated product has inventory count of "{product_inventory}".', 400
        )


def handle_exception(message, status_code=500):
    return exceptions.abort(make_response(message, status_code))
