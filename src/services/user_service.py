import jwt
import logging
from datetime import datetime, timedelta

from src.config import Config
from src.helpers import handle_exception
from src.models import User
from src.services import database_service

logger = logging.getLogger(__name__)


def create(user_instance):
    _check_for_valid_field_keys(user_instance)
    return database_service.post_entity_instance(User, user_instance)


def delete(user_id):
    return database_service.delete_entity_instance(User, user_id)


def update(user_id, user_instance):
    _check_for_valid_field_keys(user_instance, False)
    return database_service.edit_entity_instance(User, user_id, user_instance)


def get(user_id):
    return database_service.get_entity_instance_by_id(User, user_id)


def list_all(filter_by):
    return database_service.get_entity_instances(User, filter_by=filter_by)


def login(auth):
    if not auth or not auth.username or not auth.password:
        return 'Unauthorized: Could not verify user.', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}

    user = User.query.filter_by(username=auth.username).first()
    if not user or not user.check_password(auth.password):
        return 'Unauthorized: Incorrect username and/or password.', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}

    token = jwt.encode(
        {'id': str(user.id), 'exp': datetime.utcnow() + timedelta(hours=1)},
        Config.SECRET_KEY
    )
    return {'token': token.decode('UTF-8')}


def _check_for_valid_field_keys(user_instance, is_post_request=True):
    if not is_post_request:
        if not set(user_instance).issubset({'username', 'password'}):
            raise handle_exception(
                'Bad Request: You may only include the "username" and "password" fields in your PUT request.', 400
            )
        return

    if set(user_instance) != {'username', 'password'}:
        raise handle_exception(
            'Bad Request: Your POST request must include (only) the "username" and "password" fields.', 400
        )
