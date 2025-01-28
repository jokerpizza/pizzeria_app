from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))   # "YYYY-MM-DD"
    cash = db.Column(db.Float, default=0.0)
    card = db.Column(db.Float, default=0.0)
    online = db.Column(db.Float, default=0.0)

class Cost(db.Model):
    __tablename__ = 'costs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))   # "YYYY-MM-DD"
    category = db.Column(db.String(50))
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, default=0.0)
