from datetime import datetime
from .extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    unit = db.Column(db.String(20), nullable=False, default="szt")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    prices = db.relationship("ProductPrice", backref="product", lazy=True, cascade="all, delete-orphan")

class ProductPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, index=True)
    quantity = db.Column(db.Float, nullable=False, default=1.0)   # ile kupujesz w paczce
    price = db.Column(db.Numeric(10,2), nullable=False)           # cena za paczkę
    currency = db.Column(db.String(4), nullable=False, default="PLN")
    valid_from = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
