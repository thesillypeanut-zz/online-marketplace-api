from datetime import datetime
from sqlalchemy_utils import UUIDType

from src import db
from src.helpers import generate_uuid


class Cart(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cart_items = db.relationship('CartItem', backref='cart', lazy=True, cascade="delete")
    order = db.relationship('Order', backref='cart', lazy=True)

    def __repr__(self):
        return f"Cart('{self.date_created}')"

    def serialize(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "cart_item_count": len(self.cart_items),
            "is_ordered": True if self.order else False
        }


class Product(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    inventory_count = db.Column(db.Integer(), nullable=False)
    cart_items = db.relationship('CartItem', backref='product', lazy=True, cascade="delete")

    def __repr__(self):
        return f"Product('{self.title}', '{self.price}', '{self.inventory_count}')"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "inventory_count": self.inventory_count,
            "cart_item_count": len(self.cart_items)
        }


class CartItem(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantity = db.Column(db.Integer(), nullable=False)
    cart_id = db.Column(UUIDType(binary=False), db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(UUIDType(binary=False), db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f"CartItem('{self.cart_id}', '{self.product_id}', '{self.date_added}', '{self.quantity}')"

    def serialize(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "date_added": self.date_added,
            "cart_id": self.cart_id,
            "product_id": self.product_id
        }


class Order(db.Model):
    id = db.Column(UUIDType(binary=False), primary_key=True, default=generate_uuid)
    cart_id = db.Column(UUIDType(binary=False), db.ForeignKey('cart.id'))
    date_ordered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Order(''{self.cart_id}', '{self.date_ordered}')"

    def serialize(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "date_ordered": self.date_ordered
        }
