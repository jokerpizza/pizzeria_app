
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Nowe pole na hasło

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gotowka = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class Cost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class ATMDeposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
