import logging

from src.helpers import validate_cart_item_quantity_is_not_more_than_product_inventory, handle_exception
from src.models import CartItem
from src.services import database_service, cart_service, product_service

logger = logging.getLogger(__name__)


def create(cart_item_instance, current_user):
    if not current_user.carts or all([cart.order for cart in current_user.carts]):
        cart = cart_service.create(current_user.id)
        cart_id = cart['id']
    else:
        cart = [cart for cart in current_user.carts if not cart.order][0]
        cart_id = cart.id

    _check_for_valid_field_keys(cart_item_instance)

    cart_quantity = cart_item_instance['quantity']
    if cart_quantity == 0:
        raise handle_exception('Bad Request: Cart item quantity must be more than 0.', 400)

    _ensure_product_id_and_quantity_are_valid(cart_item_instance)
    cart_item_instance.update({'cart_id': cart_id})

    return database_service.post_entity_instance(CartItem, cart_item_instance)


def delete(cart_item_id):
    _ensure_cart_item_is_not_ordered(cart_item_id)
    return database_service.delete_entity_instance(CartItem, cart_item_id, False)


def update(cart_item_id, cart_item_instance):
    _check_for_valid_field_keys(cart_item_instance, False)
    _ensure_cart_item_is_not_ordered(cart_item_id)

    cart_quantity = cart_item_instance['quantity']
    if cart_quantity == 0:
        return delete(cart_item_id)

    _ensure_product_id_and_quantity_are_valid(cart_item_instance, cart_item_id)

    return database_service.edit_entity_instance(CartItem, cart_item_id, cart_item_instance, False)


def get(cart_item_id, serialize=True):
    return database_service.get_entity_instance_by_id(CartItem, cart_item_id, serialize, False)


def list_all(filter_by):
    return database_service.get_entity_instances(CartItem, filter_by=filter_by)


def _ensure_product_id_and_quantity_are_valid(cart_item_instance, cart_item_id=None):
    cart_quantity = cart_item_instance['quantity']

    if cart_item_id:
        cart_item_instance = get(cart_item_id)

    product_id = cart_item_instance['product_id']
    product = product_service.get(product_id)
    product_inventory = product['inventory_count']

    validate_cart_item_quantity_is_not_more_than_product_inventory(product_inventory, cart_quantity, product_id)


def _check_for_valid_field_keys(cart_item_instance, is_post_request=True):
    if not is_post_request:
        if set(cart_item_instance) != {'quantity'}:
            raise handle_exception('Bad Request: You can only include the "quantity" field in your PUT request.', 400)
        return

    if set(cart_item_instance) != {'quantity', 'product_id'}:
        raise handle_exception(
            'Bad Request: Please include the following fields in your POST request: "quantity", "product_id"', 400
        )


def _ensure_cart_item_is_not_ordered(cart_item_id):
    cart_item = get(cart_item_id, False)
    cart = cart_service.get(cart_item.cart_id)

    if cart['is_ordered']:
        raise handle_exception(
            f'Bad Request: You cannot delete or update cart item with id "{cart_item_id}" that is already ordered.', 400
        )
