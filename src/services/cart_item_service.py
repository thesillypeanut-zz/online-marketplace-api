import logging
from werkzeug import exceptions

from src.helpers import validate_cart_item_quantity_is_not_more_than_product_inventory
from src.models import CartItem
from src.services import database_service, cart_service, product_service

logger = logging.getLogger(__name__)


def create(cart_item_instance):
    _check_for_valid_field_keys(cart_item_instance)
    _ensure_product_id_and_quantity_are_valid(cart_item_instance)

    if cart_item_instance.get('cart_id'):
        _ensure_cart_id_is_valid(cart_item_instance['cart_id'])
        return database_service.post_entity_instance(CartItem, cart_item_instance)

    cart = cart_service.create()
    logger.info(f'Request does not contain a "cart_id". Successfully created a new cart.')
    cart_item_instance.update({'cart_id': cart['id']})

    return database_service.post_entity_instance(CartItem, cart_item_instance)


def delete(cart_item_id):
    return database_service.delete_entity_instance(CartItem, cart_item_id)


def update(cart_item_id, cart_item_instance):
    _check_for_valid_field_keys(cart_item_instance, False)
    _ensure_product_id_and_quantity_are_valid(cart_item_instance, cart_item_id)

    return database_service.edit_entity_instance(CartItem, cart_item_id, cart_item_instance)


def get(cart_item_id):
    return database_service.get_entity_instance_by_id(CartItem, cart_item_id)


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


def _ensure_cart_id_is_valid(cart_id):
    try:
        cart_service.get(cart_id)
    except exceptions.NotFound:
        raise exceptions.BadRequest('If you don\'t have a cart created, do not include the "cart_id" field in '
                                    'your request. A cart will be created for you.')


def _check_for_valid_field_keys(cart_item_instance, is_post_request=True):
    if not is_post_request:
        if set(cart_item_instance) != {'quantity'}:
            raise exceptions.BadRequest('You can only include the "quantity" field in your PUT request.')
        return


    if cart_item_instance.get('date_added'):
        raise exceptions.BadRequest('Do not include the "date_added" field in your POST request. '
                                    'This is auto-generated at the time of your request.')

    if not {'quantity', 'product_id'}.issubset(cart_item_instance):
        raise exceptions.BadRequest('Please include the following fields in your POST request: '
                                    '"quantity", "product_id"')
