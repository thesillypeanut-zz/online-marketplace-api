import logging
from datetime import datetime

from src import constants
from src.models import Cart
from src.services import database_service


def create_cart(cart_instance):
    _ensure_date_created_field_is_valid(cart_instance)
    return database_service.post_entity_instance(Cart, cart_instance)


def delete_cart(cart_id):
    return database_service.delete_entity_instance(Cart, cart_id)


def edit_cart(cart_id, cart_instance):
    _ensure_date_created_field_is_valid(cart_instance)
    return database_service.edit_entity_instance(Cart, cart_id, cart_instance)


def get_cart(cart_id):
    return database_service.get_entity_instance_by_id(Cart, cart_id)


def get_carts():
    return database_service.get_entity_instances(Cart, Cart.date_created)


def _ensure_date_created_field_is_valid(cart_instance):
    if cart_instance.get('date_created'):
        try:
            cart_instance['date_created'] = datetime.strptime(cart_instance['date_created'], constants.DATETIME_FORMAT)
        except ValueError:
            logging.error(f'Value for "date_created" field must match format: {constants.DATETIME_FORMAT}')
            raise
