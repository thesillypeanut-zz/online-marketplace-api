import logging

from src.helpers import handle_exception
from src.models import Product
from src.services import database_service, cart_item_service

logger = logging.getLogger(__name__)


def create(product_instance):
    _check_for_valid_field_keys(product_instance)
    return database_service.post_entity_instance(Product, product_instance)


def delete(product_id):
    return database_service.delete_entity_instance(Product, product_id)


def update(product_id, product_instance, except_cart_item_id=None):
    _check_for_valid_field_keys(product_instance, False)

    if product_instance.get('inventory_count'):
        product = get(product_id, False)
        updated_inventory_count = product_instance['inventory_count']

        for item in product.cart_items:
            cart_item_id = item.id

            # auto-update cart item quantities (might not be best user experience)
            if cart_item_id != except_cart_item_id and item.quantity > updated_inventory_count:
                cart_item_service.update(cart_item_id, {'quantity': updated_inventory_count})
                logger.info(f'Cart item with id "{cart_item_id}" was updated to have a quantity of '
                            f'{updated_inventory_count}.')

    return database_service.edit_entity_instance(Product, product_id, product_instance)


def get(product_id, serialize=True):
    return database_service.get_entity_instance_by_id(Product, product_id, serialize)


def list_all(filter_by):
    return database_service.get_entity_instances(Product, filter_by=filter_by)


def list_all_available():
    products = Product.query.filter(Product.inventory_count > 0).all()
    return [product.serialize() for product in products]


def _check_for_valid_field_keys(product_instance, is_post_request=True):
    if not is_post_request:
        if not set(product_instance).issubset({'title', 'inventory_count', 'price'}):
            raise handle_exception(
                'Bad Request: Your PUT request can only include the "title", "inventory_count" and "price" fields.', 400
            )
        return

    if set(product_instance) != {'title', 'inventory_count', 'price'}:
        raise handle_exception(
            'Bad Request: Your POST request must include (only) the "title", "inventory_count" and "price" fields.', 400
        )
