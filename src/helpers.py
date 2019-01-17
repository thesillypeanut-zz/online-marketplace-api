import uuid
from werkzeug import exceptions


def generate_uuid():
    return uuid.uuid4()


def validate_cart_item_quantity_is_not_more_than_product_inventory(product_inventory, item_quantity, product_id):
    if product_inventory < item_quantity:
        raise exceptions.BadRequest(f'Cannot add product with id "{product_id}" of quantity "{item_quantity}". '
                                    f'The associated product has inventory count of "{product_inventory}".')
