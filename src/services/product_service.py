from src.models import Product
from src.services import database_service


def create(product_instance):
    return database_service.post_entity_instance(Product, product_instance)


def delete(product_id):
    return database_service.delete_entity_instance(Product, product_id)


def update(product_id, product_instance):
    return database_service.edit_entity_instance(Product, product_id, product_instance)


def get(product_id):
    return database_service.get_entity_instance_by_id(Product, product_id)


def list_all(filter_by):
    return database_service.get_entity_instances(Product, filter_by=filter_by)
