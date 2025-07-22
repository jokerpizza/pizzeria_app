from datetime import datetime
from .extensions import db

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    unit = db.Column(db.String(16), nullable=False, default="szt")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    prices = db.relationship("ProductPrice", backref="product", lazy="dynamic", cascade="all, delete-orphan")

    def current_price(self):
        return self.prices.order_by(ProductPrice.valid_from.desc()).first()

class ProductPrice(db.Model):
    __tablename__ = "product_price"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    total_net = db.Column(db.Numeric(12,2), nullable=False)
    unit_net = db.Column(db.Numeric(12,4), nullable=False)
    currency = db.Column(db.String(8), default="PLN")
    supplier = db.Column(db.String(255))
    invoice_number = db.Column(db.String(64))
    valid_from = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
