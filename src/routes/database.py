from src import constants
from src.routes.decorators import json_response
from src.services import database_service

_DB_URL_PATH = f'{constants.BASE_URL_PATH}/db'

def add_routes(app):
    app.add_url_rule(
        rule=f'{_DB_URL_PATH}/init',
        view_func=init_db,
        endpoint=init_db.__name__
    ),
    app.add_url_rule(
        rule=f'{_DB_URL_PATH}/fill',
        view_func=fill_db,
        endpoint=fill_db.__name__
    )


@json_response(204)
def init_db():
    return database_service.init()


@json_response(200)
def fill_db():
    return database_service.fill()
