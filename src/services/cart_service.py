from src.models import Cart
from src.services import database_service


def create(customer_id):
    return database_service.post_entity_instance(Cart, {'customer_id': customer_id})


def delete(cart_id):
    cart = get(cart_id)
    if cart['is_ordered']:
        return f'Bad Request: You cannot delete cart with id "{cart_id}" that has an associated order.', 400

    return database_service.delete_entity_instance(Cart, cart_id)


def get(cart_id, serialize=True):
    return database_service.get_entity_instance_by_id(Cart, cart_id, serialize)


def list_all(filter_by):
    return database_service.get_entity_instances(Cart, Cart.date_created, filter_by)
