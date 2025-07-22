from datetime import datetime
from .extensions import db

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    unit = db.Column(db.String(20), nullable=False, default="szt")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    prices = db.relationship("ProductPrice", backref="product", cascade="all, delete-orphan")

class ProductPrice(db.Model):
    __tablename__ = "product_price"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, index=True)
    price = db.Column(db.Numeric(10,2), nullable=False)
    quantity = db.Column(db.Numeric(10,3), nullable=False, default=1)
    currency = db.Column(db.String(3), nullable=False, default="PLN")
    valid_from = db.Column(db.Date, nullable=False, default=datetime.utcnow)

def ensure_tables():
    # create tables if they do not exist (fallback when migrations missing)
    db.create_all()
