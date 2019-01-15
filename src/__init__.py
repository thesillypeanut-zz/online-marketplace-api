from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '6aebb273b8ed6f620238a539c962f934'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from src.routes import cart, product

cart.add_routes(app)
product.add_routes(app)
