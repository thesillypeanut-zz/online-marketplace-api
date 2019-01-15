from datetime import datetime
from src import db


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cart_items = db.relationship('CartItem', backref='cart', lazy=True)
    order = db.relationship('Order', backref='cart', lazy=True)

    def __repr__(self):
        return f"Cart('{self.date_created}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subtotal = db.Column(db.Float(), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    date_ordered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Order('{self.subtotal}', '{self.cart_id}', '{self.date_ordered}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    inventory_count = db.Column(db.Integer(), nullable=False)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)

    def __repr__(self):
        return f"Product('{self.title}', '{self.price}', '{self.inventory_count}')"


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"CartItem('{self.cart_id}', '{self.product_id}', '{self.date_added}')"
