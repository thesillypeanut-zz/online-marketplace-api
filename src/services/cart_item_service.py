from src.models import CartItem
from src.services import database_service


def create(cart_item_instance):
    return database_service.post_entity_instance(CartItem, cart_item_instance)


def delete(cart_item_id):
    return database_service.delete_entity_instance(CartItem, cart_item_id)


def update(cart_item_id, cart_item_instance):
    return database_service.edit_entity_instance(CartItem, cart_item_id, cart_item_instance)


def get(cart_item_id):
    return database_service.get_entity_instance_by_id(CartItem, cart_item_id)


def list_all(filter_by):
    return database_service.get_entity_instances(CartItem, filter_by=filter_by)
