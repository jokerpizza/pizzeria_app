
import os
from datetime import date
import calendar

from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Sale, Cost
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzeria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super-secret-key'

db.init_app(app)

with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

# Rejestracja, logowanie, wylogowanie
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Taki użytkownik już istnieje!"
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        return "Nieprawidłowe dane logowania!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dodawanie, edycja i usuwanie sprzedaży
@app.route('/add_sale', methods=['GET','POST'])
@login_required
def add_sale():
    if request.method == 'POST':
        sale_date = request.form['date']
        dine_in = float(request.form['dine_in'] or 0)
        delivery = float(request.form['delivery'] or 0)
        other = float(request.form['other'] or 0)
        new_sale = Sale(date=sale_date, dine_in=dine_in, delivery=delivery, other=other)
        db.session.add(new_sale)
        db.session.commit()
        return redirect(url_for('sales_list'))
    return render_template('add_sale.html')

@app.route('/sales')
@login_required
def sales_list():
    sales = Sale.query.order_by(Sale.date.desc()).all()
    return render_template('sales_list.html', sales=sales)

@app.route('/edit_sale/<int:sale_id>', methods=['GET', 'POST'])
@login_required
def edit_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    if request.method == 'POST':
        sale.date = request.form['date']
        sale.dine_in = float(request.form['dine_in'] or 0)
        sale.delivery = float(request.form['delivery'] or 0)
        sale.other = float(request.form['other'] or 0)
        db.session.commit()
        return redirect(url_for('sales_list'))
    return render_template('edit_sale.html', sale=sale)

@app.route('/delete_sale/<int:sale_id>', methods=['POST'])
@login_required
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    return redirect(url_for('sales_list'))

# Dodawanie, edycja i usuwanie kosztów
@app.route('/add_cost', methods=['GET','POST'])
@login_required
def add_cost():
    if request.method == 'POST':
        cost_date = request.form['date']
        category = request.form['category']
        description = request.form['description']
        amount = float(request.form['amount'] or 0)
        new_cost = Cost(date=cost_date, category=category, description=description, amount=amount)
        db.session.add(new_cost)
        db.session.commit()
        return redirect(url_for('costs_list'))
    return render_template('add_cost.html')

@app.route('/costs')
@login_required
def costs_list():
    costs = Cost.query.order_by(Cost.date.desc()).all()
    return render_template('costs_list.html', costs=costs)

@app.route('/edit_cost/<int:cost_id>', methods=['GET', 'POST'])
@login_required
def edit_cost(cost_id):
    cost = Cost.query.get_or_404(cost_id)
    if request.method == 'POST':
        cost.date = request.form['date']
        cost.category = request.form['category']
        cost.description = request.form['description']
        cost.amount = float(request.form['amount'] or 0)
        db.session.commit()
        return redirect(url_for('costs_list'))
    return render_template('edit_cost.html', cost=cost)

@app.route('/delete_cost/<int:cost_id>', methods=['POST'])
@login_required
def delete_cost(cost_id):
    cost = Cost.query.get_or_404(cost_id)
    db.session.delete(cost)
    db.session.commit()
    return redirect(url_for('costs_list'))

if __name__ == '__main__':
    app.run(debug=True)
