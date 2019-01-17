import logging
from datetime import datetime

from src import constants
from src.models import Order
from src.services import database_service


def create(order_instance):
    _ensure_date_ordered_field_is_valid(order_instance)
    return database_service.post_entity_instance(Order, order_instance)


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
