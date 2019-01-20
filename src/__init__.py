from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from src.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    from src.models import Cart, Product, CartItem, Order, User

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    db.drop_all(app=app)
    db.create_all(app=app)

    from src.routes import cart, product, cart_item, order, user, database
    cart.add_routes(app)
    product.add_routes(app)
    cart_item.add_routes(app)
    order.add_routes(app)
    user.add_routes(app)
    database.add_routes(app)

    return app
