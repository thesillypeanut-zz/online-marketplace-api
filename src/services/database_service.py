import logging
from werkzeug import exceptions

from src import db


def delete_entity_instance(db_model, entity_id):
    try:
        entity = db_model.query.get_or_404(entity_id)
    except exceptions.NotFound:
        logging.error(f'Entity type "{db_model.__name__}" with id "{entity_id}" is not found.')
        return '', 404

    db.session.delete(entity)
    db.session.commit()
    return '', 204


def edit_entity_instance(db_model, entity_id, updated_entity_instance):
    try:
        entity = db_model.query.get_or_404(entity_id)
    except exceptions.NotFound:
        logging.error(f'Entity type "{db_model.__name__}" with id "{entity_id}" is not found.')
        raise

    for key in updated_entity_instance:
        setattr(entity, key, updated_entity_instance[key])

    db.session.commit()

    return entity.serialize()


def filter_by(db_model, filter_by):
    try:
        entities = db_model.query.filter_by(**filter_by).all()
    except Exception:
        logging.error(f'Exception encountered while querying "{db_model.__name__}" filtered by "{filter_by}".')
        raise

    return [entity.serialize() for entity in entities]


def get_entity_instances(db_model, order_by=None):
    try:
        entities = db_model.query.order_by(order_by).all()
    except Exception:
        logging.error(f'Exception encountered while querying "{db_model.__name__}" ordered by "{order_by}".')
        raise

    return [entity.serialize() for entity in entities]


def get_entity_instance_by_id(db_model, entity_id):
    try:
        entity = db_model.query.get_or_404(entity_id)
    except exceptions.NotFound:
        logging.error(f'Entity type "{db_model.__name__}" with id "{entity_id}" is not found.')
        raise

    return entity.serialize()


def post_entity_instance(db_model, entity_instance):
    entity = db_model(**entity_instance) if entity_instance else db_model()
    db.session.add(entity)
    db.session.commit()

    return entity.serialize()
