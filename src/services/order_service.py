import logging
from datetime import datetime
from werkzeug import exceptions

from src import constants
from src.models import Order, CartItem, Product
from src.services import database_service


def create(order_instance):
    _ensure_date_ordered_field_is_valid(order_instance)
    order = database_service.post_entity_instance(Order, order_instance)

    cart_id = order['cart_id']
    cart_items = database_service.get_entity_instances(CartItem, filter_by={'cart_id': cart_id})

    for item in cart_items:
        product_id = item['product_id']
        product = database_service.get_entity_instance_by_id(Product, product_id)
        updated_inventory_count = product['inventory_count'] - item['inventory_count']

        if updated_inventory_count < 0:
            raise exceptions.BadRequest('Cannot order qu')

        database_service.edit_entity_instance(Product, {'inventory_count': product})

    return order


def delete(order_id):
    return database_service.delete_entity_instance(Order, order_id)


def get(order_id):
    return database_service.get_entity_instance_by_id(Order, order_id)


def list_all():
    return database_service.get_entity_instances(Order, Order.date_ordered)


def _ensure_date_ordered_field_is_valid(order_instance):
    if order_instance and order_instance.get('date_ordered'):
        try:
            order_instance['date_ordered'] = datetime.strptime(order_instance['date_ordered'], constants.DATETIME_FORMAT)
        except ValueError:
            logging.error(f'Value for "date_ordered" field must match format: {constants.DATETIME_FORMAT}')
            raise
