from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SafeTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # Format YYYY-MM-DD
    type = db.Column(db.String(20), nullable=False)  # "Wpłata" lub "Wypłata"
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, date, type, amount):
        self.date = date
        self.type = type
        self.amount = amount
