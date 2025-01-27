
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
    else:
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
        else:
            return "Nieprawidłowe dane logowania!"
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

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
    else:
        return render_template('add_sale.html')

@app.route('/sales')
@login_required
def sales_list():
    sales = Sale.query.order_by(Sale.date.desc()).all()
    return render_template('sales_list.html', sales=sales)

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
    else:
        return render_template('add_cost.html')

@app.route('/costs')
@login_required
def costs_list():
    costs = Cost.query.order_by(Cost.date.desc()).all()
    return render_template('costs_list.html', costs=costs)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    today = date.today()
    current_year = today.year
    current_month = today.month

    selected_year = request.args.get('year', current_year, type=int)
    selected_month = request.args.get('month', current_month, type=int)

    selected_year_month = f"{selected_year}-{selected_month:02d}"

    _, num_days_in_month = calendar.monthrange(selected_year, selected_month)
    daily_sales = [0.0] * num_days_in_month
    daily_costs = [0.0] * num_days_in_month

    sales = Sale.query.all()
    costs = Cost.query.all()

    for s in sales:
        if s.date and s.date.startswith(selected_year_month):
            day_str = s.date[8:10]
            try:
                day_int = int(day_str)
                daily_sales[day_int - 1] += (s.dine_in + s.delivery + s.other)
            except ValueError:
                pass

    for c in costs:
        if c.date and c.date.startswith(selected_year_month):
            day_str = c.date[8:10]
            try:
                day_int = int(day_str)
                daily_costs[day_int - 1] += c.amount
            except ValueError:
                pass

    labels = list(range(1, num_days_in_month + 1))

    return render_template(
        'dashboard.html',
        labels=labels,
        daily_sales=daily_sales,
        daily_costs=daily_costs,
        selected_year=selected_year,
        selected_month=selected_month,
    )
