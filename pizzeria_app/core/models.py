from datetime import datetime
from .extensions import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    unit = db.Column(db.String(20), nullable=False, default='szt')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # last price convenience relationship
    prices = db.relationship("ProductPrice", backref="product", cascade="all, delete-orphan")

    def current_price(self):
        if not self.prices:
            return None
        return max(self.prices, key=lambda p: p.valid_from).price_per_unit

class ProductPrice(db.Model):
    __tablename__ = 'product_price'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price_per_unit = db.Column(db.Numeric(10,2), nullable=False)
    valid_from = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
