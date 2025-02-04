from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()



class RolePermissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __table_args__ = {'extend_existing': True}
    role = db.Column(db.String(20), nullable=True)  # Role-based permissions
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # User-specific permissions
    permission = db.Column(db.String(50), nullable=False)

class RolePermissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __table_args__ = {'extend_existing': True}
    role = db.Column(db.String(20), nullable=True)
    permission = db.Column(db.String(50), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='Pracownik', nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))   # "YYYY-MM-DD"
    gotowka = db.Column(db.Float, default=0.0)
    przelew = db.Column(db.Float, default=0.0)
    zaplacono = db.Column(db.Float, default=0.0)
    delivery = db.Column(db.Float, default=0.0)
    other = db.Column(db.Float, default=0.0)


class CostCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Cost(db.Model):
    payment_method = db.Column(db.String(20), nullable=False, default='Gotówka')
    __tablename__ = 'costs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))   # "YYYY-MM-DD"
    category = db.Column(db.String(50))
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, default=0.0)


from datetime import datetime
from pizzeria_app import db

class ATMDeposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ATMDeposit {self.amount} on {self.date}>"
