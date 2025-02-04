
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from models import db, User, Sale, Cost, ATMDeposit

@app.route('/')
def index():
    return "Pizzeria App działa!"

@app.route('/safe', methods=['GET'])
def safe():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    sales = Sale.query.all()
    costs = Cost.query.filter_by(payment_method="Gotówka").all()
    atm_deposits = ATMDeposit.query.all()

    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        sales = [s for s in sales if start_date <= s.date <= end_date]
        costs = [c for c in costs if start_date <= c.date <= end_date]
        atm_deposits = [a for a in atm_deposits if start_date <= a.date <= end_date]

    total_cash_in = sum(s.gotowka for s in sales) + sum(a.amount for a in atm_deposits)
    total_cash_out = sum(c.amount for c in costs)

    current_safe_balance = total_cash_in - total_cash_out

    transactions = (
        [(s.date, "Sprzedaż", s.gotowka) for s in sales if s.gotowka > 0] +
        [(c.date, "Koszt", -c.amount) for c in costs] +
        [(a.date, "Wpłata bankomat", a.amount) for a in atm_deposits]
    )

    transactions.sort(reverse=True, key=lambda x: x[0])

    return render_template(
        'safe.html',
        current_safe_balance=current_safe_balance,
        transactions=transactions
    )

@app.route('/deposit-atm', methods=['POST'])
def deposit_atm():
    amount = request.form.get("amount")
    if amount:
        amount = float(amount)
        new_deposit = ATMDeposit(amount=amount, date=datetime.utcnow())
        db.session.add(new_deposit)
        db.session.commit()
    return redirect(url_for('safe'))

if __name__ == "__main__":
    app.run(debug=True)
