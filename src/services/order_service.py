from werkzeug import exceptions

from src.helpers import validate_cart_item_quantity_is_not_more_than_product_inventory
from src.models import Order
from src.services import database_service, cart_service, product_service


def create(order_instance):
    _check_for_valid_field_keys(order_instance)

    cart_id = order_instance['cart_id']
    cart = cart_service.get(cart_id, False)

    _ensure_order_quantities_are_valid(cart)
    order = database_service.post_entity_instance(Order, order_instance)

    for item in cart.cart_items:
        product_id = item.product_id
        product = product_service.get(product_id)
        product_service.update(item.product_id, {'inventory_count': product['inventory_count'] - item.quantity})

    return order


def get(order_id):
    return database_service.get_entity_instance_by_id(Order, order_id)


def list_all():
    return database_service.get_entity_instances(Order, Order.date_ordered)


def _check_for_valid_field_keys(order_instance):
    if set(order_instance) != {'cart_id'}:
        raise exceptions.BadRequest('Your POST request must include (only) the "cart_id" field.')


def _ensure_order_quantities_are_valid(cart):
    cart_id = cart['id']

    if len(cart.cart_items) == 0:
        raise exceptions.BadRequest(f'Cart with id "{cart_id}" does not contain any items to order. Select a cart that '
                                    f'contains at least one item.')

    for item in cart.cart_items:
        product_id = item.product_id
        product = product_service.get(product_id)
        product_inventory = product['inventory_count']
        order_quantity = item.quantity

        validate_cart_item_quantity_is_not_more_than_product_inventory(product_inventory, order_quantity, product_id)
