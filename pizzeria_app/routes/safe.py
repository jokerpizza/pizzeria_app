from flask import Blueprint, render_template, request, redirect, url_for, send_file
from models import db, SafeTransaction
from datetime import date
import pandas as pd
import io

safe_bp = Blueprint("safe", __name__)

@safe_bp.route("/safe", methods=["GET", "POST"])
def safe():
    if request.method == "POST":
        amount = float(request.form["amount"])
        transaction_type = request.form["type"]
        new_transaction = SafeTransaction(date.today().strftime("%Y-%m-%d"), transaction_type, amount)

        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for("safe.safe"))

    transactions = SafeTransaction.query.order_by(SafeTransaction.date.desc()).all()
    current_balance = sum(t.amount if t.type == "Wpłata" else -t.amount for t in transactions)
    total_income = sum(t.amount for t in transactions if t.type == "Wpłata")
    total_expenses = sum(t.amount for t in transactions if t.type == "Wypłata")

    return render_template("safe.html", current_safe_balance=current_balance, 
                           recent_transactions=transactions, total_income=total_income, total_expenses=total_expenses)

@safe_bp.route("/export_safe_data")
def export_safe_data():
    transactions = SafeTransaction.query.all()
    df = pd.DataFrame([(t.date, t.type, t.amount) for t in transactions], columns=["Data", "Typ", "Kwota"])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sejf")

    output.seek(0)
    return send_file(output, download_name="safe_data.xlsx", as_attachment=True)
