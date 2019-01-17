from src.models import Cart
from src.services import database_service


def create():
    return database_service.post_entity_instance(Cart)


def delete(cart_id):
    return database_service.delete_entity_instance(Cart, cart_id)


def get(cart_id):
    return database_service.get_entity_instance_by_id(Cart, cart_id)


def list_all(filter_by):
    return database_service.get_entity_instances(Cart, Cart.date_created, filter_by)
