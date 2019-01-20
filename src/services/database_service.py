import logging
from werkzeug import exceptions

from src import db
from src.helpers import handle_exception
from src.models import Product

logger = logging.getLogger(__name__)


def delete_entity_instance(db_model, entity_id, is_id_primary_key=True):
    try:
        entity = (
            db_model.query.get_or_404(entity_id)
            if is_id_primary_key else
            db_model.query.filter_by(id=entity_id).first()
        )
    except exceptions.NotFound:
        raise handle_exception(f'Entity type "{db_model.__name__}" with id "{entity_id}" is not found.', 404)

    db.session.delete(entity)
    db.session.commit()
    return '', 204


def edit_entity_instance(db_model, entity_id, updated_entity_instance, is_id_primary_key=True):
    try:
        entity = (
            db_model.query.get_or_404(entity_id)
            if is_id_primary_key else
            db_model.query.filter_by(id=entity_id).first()
        )
    except exceptions.NotFound:
        raise handle_exception(f'Entity type "{db_model.__name__}" with id "{entity_id}" is not found.', 404)

    for key in updated_entity_instance:
        setattr(entity, key, updated_entity_instance[key])

    db.session.commit()

    return entity.serialize()


def fill():
    db.create_all()

    product_1 = Product(title='Wolfsbane Potion', price=10.40, inventory_count=300)
    product_2 = Product(title='Polyjuice Potion', price=20, inventory_count=500)
    product_3 = Product(title='Felix Felicis', price=2.30, inventory_count=100)
    product_4 = Product(title='Confusing Concoction', price=8.99, inventory_count=102)
    product_5 = Product(title='Hiccoughing Potion', price=3.11, inventory_count=100)
    product_6 = Product(title='Pepperup Potion', price=0.99, inventory_count=900)
    product_7 = Product(title='Draught of Peace', price=1.12, inventory_count=80)
    product_8 = Product(title='Ageing Potion', price=5.30, inventory_count=100)
    product_9 = Product(title='Unicorn Blood', price=57.88, inventory_count=5)
    product_10 = Product(title='Veritaserum', price=31.20, inventory_count=10)

    db.session.add(product_1)
    db.session.add(product_2)
    db.session.add(product_3)
    db.session.add(product_4)
    db.session.add(product_5)
    db.session.add(product_6)
    db.session.add(product_7)
    db.session.add(product_8)
    db.session.add(product_9)
    db.session.add(product_10)

    db.session.commit()
    return '', 204


def get_entity_instances(db_model, order_by=None, filter_by=None):
    try:
        if filter_by:
            entities = (
                db_model.query.order_by(order_by).filter_by(**filter_by.to_dict()).all()
                if type(filter_by) != dict else db_model.query.order_by(order_by).filter_by(**filter_by).all()
            )
        else:
            entities = db_model.query.order_by(order_by).all()
    except Exception:
        raise handle_exception(f'Exception encountered while querying "{db_model.__name__}" ordered by "{order_by}" '
                     f'filtered by "{filter_by}".')

    return [entity.serialize() for entity in entities]


def get_entity_instance_by_id(db_model, entity_id, serialize=True, is_id_primary_key=True):
    try:
        entity = (
            db_model.query.get_or_404(entity_id)
            if is_id_primary_key else
            db_model.query.filter_by(id=entity_id).first()
        )

    except exceptions.NotFound:
        raise handle_exception(f'Entity type "{db_model.__name__}" with id "{entity_id}" is not found.', 404)

    if not serialize:
        return entity

    return entity.serialize()


def init():
    db.drop_all()
    db.create_all()
    return '', 204


def post_entity_instance(db_model, entity_instance=None):
    entity = db_model(**entity_instance) if entity_instance else db_model()
    db.session.add(entity)
    db.session.commit()

    return entity.serialize()
