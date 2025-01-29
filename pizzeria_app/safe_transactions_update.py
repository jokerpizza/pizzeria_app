from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import sys
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzeria.db'  # Dostosuj bazę danych
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Wyłączenie ostrzeżeń
app.secret_key = 'super-secret-key'
db = SQLAlchemy(app)

# MODELE BAZY DANYCH
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    gotowka = db.Column(db.Float, default=0.0)

class Cost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    amount = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(20), nullable=False, default='Gotówka')

class SafeTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), default=date.today().strftime("%Y-%m-%d"))
    type = db.Column(db.String(10), nullable=False)  # "Wpłata" lub "Wypłata"
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

# FUNKCJA OBLICZAJĄCA STAN SEJFU
def get_safe_balance():
    try:
        total_cash_in = sum(s.gotowka for s in Sale.query.all())
        total_cash_out = sum(c.amount for c in Cost.query.filter_by(payment_method="Gotówka").all())
        transactions = SafeTransaction.query.all()
    
        manual_deposits = sum(t.amount for t in transactions if t.type == "Wpłata")
        manual_withdrawals = sum(t.amount for t in transactions if t.type == "Wypłata")
    
        return total_cash_in + manual_deposits - (total_cash_out + manual_withdrawals)
    except Exception as e:
        sys.stderr.write(f"Błąd obliczania stanu sejfu: {str(e)}\n")
        return 0.0

# PANEL SEJFU
@app.route('/safe', methods=['GET', 'POST'])
def safe():
    current_safe_balance = get_safe_balance()
    transactions = SafeTransaction.query.order_by(SafeTransaction.date.desc()).all()
    return render_template('safe.html', current_safe_balance=current_safe_balance, transactions=transactions)

# DODAWANIE TRANSAKCJI DO SEJFU
@app.route('/safe_transaction', methods=['POST'])
def safe_transaction():
    try:
        transaction_type = request.form['type']
        amount = float(request.form['amount'])
        description = request.form['description']
    
        new_transaction = SafeTransaction(type=transaction_type, amount=amount, description=description)
        db.session.add(new_transaction)
        db.session.commit()
    except Exception as e:
        sys.stderr.write(f"Błąd dodawania transakcji do sejfu: {str(e)}\n")
    
    return redirect(url_for('safe'))

# NOWOCZESNY INTERFEJS UŻYTKOWNIKA (HTML + CSS)
@app.route('/safe_ui')
def safe_ui():
    return render_template('safe_ui.html', balance=get_safe_balance(), transactions=SafeTransaction.query.order_by(SafeTransaction.date.desc()).all())

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    except Exception as e:
        sys.stderr.write(f"Błąd uruchomienia aplikacji: {str(e)}\n")
        sys.exit(1)
