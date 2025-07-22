from .extensions import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    unit = db.Column(db.String(20), nullable=False, default='szt')  # kg, l, szt
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    price_per_unit = db.Column(db.Numeric(10,2), nullable=False)  # buying price for given unit

    def __repr__(self):
        return f"<Product {self.name}>"

class ProductPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    valid_from = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref=db.backref('prices', lazy=True, order_by='ProductPrice.valid_from.desc()'))
