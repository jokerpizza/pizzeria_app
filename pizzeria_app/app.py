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

# Klucz do sesji – w produkcji trzymaj go w bezpiecznym miejscu (np. zmienna środowiskowa)
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

# ---------------------------
# Rejestracja / Logowanie / Wylogowanie
# ---------------------------
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

# ---------------------------
# Formularze i listy Sprzedaży
# ---------------------------
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

# ---------------------------
# Formularze i listy Kosztów
# ---------------------------
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

# ---------------------------
# Status Finansowy + Prognoza
# ---------------------------

@app.route('/finance_status', methods=['GET'])
@login_required
def finance_status():
    # Pobranie parametrów month i year z GET (domyślnie bieżący miesiąc i rok)
    today = date.today()
    current_year = today.year
    current_month = today.month

    selected_year = request.args.get('year', current_year, type=int)
    selected_month = request.args.get('month', current_month, type=int)
    
    # Sformatuj wybrany rok i miesiąc
    selected_year_month = f"{selected_year}-{selected_month:02d}"

    # Zliczamy sprzedaż i koszty dla wybranego miesiąca
    sales = Sale.query.all()
    costs = Cost.query.all()

    monthly_sales = 0
    monthly_costs = 0

    for s in sales:
        if s.date and s.date.startswith(selected_year_month):
            monthly_sales += (s.dine_in + s.delivery + s.other)

    for c in costs:
        if c.date and c.date.startswith(selected_year_month):
            monthly_costs += c.amount

    current_profit = monthly_sales - monthly_costs

    # Obliczenia dla prognozy
    _, num_days_in_month = calendar.monthrange(selected_year, selected_month)
    day_of_month = today.day if selected_month == current_month and selected_year == current_year else num_days_in_month

    if day_of_month > 0:
        average_daily_profit = current_profit / day_of_month
        projected_month_end = average_daily_profit * num_days_in_month
    else:
        average_daily_profit = 0
        projected_month_end = 0

    return render_template(
        "finance_status.html",
        current_profit=current_profit,
        average_daily_profit=average_daily_profit,
        projected_month_end=projected_month_end,
        selected_year=selected_year,
        selected_month=selected_month,
    )

@login_required
def finance_status():
    # Określ bieżący rok-miesiąc (np. "2025-01")
    today = date.today()
    current_year_month = today.strftime("%Y-%m")

    # Zliczamy sprzedaż i koszty w tym miesiącu
    sales = Sale.query.all()
    costs = Cost.query.all()

    monthly_sales = 0
    monthly_costs = 0

    for s in sales:
        if s.date and s.date.startswith(current_year_month):
            monthly_sales += (s.dine_in + s.delivery + s.other)

    for c in costs:
        if c.date and c.date.startswith(current_year_month):
            monthly_costs += c.amount

    current_profit = monthly_sales - monthly_costs

    day_of_month = today.day
    _, num_days_in_month = calendar.monthrange(today.year, today.month)

    if day_of_month > 0:
        average_daily_profit = current_profit / day_of_month
        projected_month_end = average_daily_profit * num_days_in_month
    else:
        average_daily_profit = 0
        projected_month_end = 0

    return render_template(
        "finance_status.html",
        current_profit=current_profit,
        average_daily_profit=average_daily_profit,
        projected_month_end=projected_month_end,
        current_year_month=current_year_month
    )

# ---------------------------
# DASHBOARD Z WYKRESAMI (Chart.js)
# ---------------------------

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # Pobranie parametrów month i year z GET (domyślnie bieżący miesiąc i rok)
    today = date.today()
    current_year = today.year
    current_month = today.month

    selected_year = request.args.get('year', current_year, type=int)
    selected_month = request.args.get('month', current_month, type=int)
    
    # Sformatuj wybrany rok i miesiąc
    selected_year_month = f"{selected_year}-{selected_month:02d}"

    # Ile dni w wybranym miesiącu
    _, num_days_in_month = calendar.monthrange(selected_year, selected_month)
    daily_sales = [0.0] * num_days_in_month
    daily_costs = [0.0] * num_days_in_month

    sales = Sale.query.all()
    costs = Cost.query.all()

    for s in sales:
        if s.date and s.date.startswith(selected_year_month):
            day_str = s.date[8:10]  # np. '05'
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

@login_required
def dashboard():
    """
    Strona z wykresami:
    - Pobieramy sprzedaż i koszty z bieżącego miesiąca
    - Grupujemy je day -> sales_sum, day -> cost_sum
    - Wyświetlamy wykres w dashboard.html
    """
    today = date.today()
    current_year_month = today.strftime("%Y-%m")
    # Ile dni w obecnym miesiącu
    _, num_days_in_month = calendar.monthrange(today.year, today.month)

    daily_sales = [0.0] * num_days_in_month
    daily_costs = [0.0] * num_days_in_month

    sales = Sale.query.all()
    costs = Cost.query.all()

    for s in sales:
        if s.date and s.date.startswith(current_year_month):
            day_str = s.date[8:10]  # np. '05'
            try:
                day_int = int(day_str)
                daily_sales[day_int - 1] += (s.dine_in + s.delivery + s.other)
            except:
                pass

    for c in costs:
        if c.date and c.date.startswith(current_year_month):
            day_str = c.date[8:10]
            try:
                day_int = int(day_str)
                daily_costs[day_int - 1] += c.amount
            except:
                pass

    labels = list(range(1, num_days_in_month + 1))

    return render_template(
        'dashboard.html',
        labels=labels,
        daily_sales=daily_sales,
        daily_costs=daily_costs,
        current_year_month=current_year_month
    )


if __name__ == '__main__':
    app.run(debug=True)

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


@app.route('/cost_summary', methods=['GET'])
@login_required
def cost_summary():
    # Pobranie parametrów month i year z GET (domyślnie bieżący miesiąc i rok)
    today = date.today()
    current_year = today.year
    current_month = today.month

    selected_year = request.args.get('year', current_year, type=int)
    selected_month = request.args.get('month', current_month, type=int)
    
    # Sformatuj wybrany rok i miesiąc
    selected_year_month = f"{selected_year}-{selected_month:02d}"

    # Grupowanie kosztów według kategorii dla wybranego miesiąca
    costs = Cost.query.filter(Cost.date.startswith(selected_year_month)).all()
    summary = {}
    for cost in costs:
        category = cost.category
        summary[category] = summary.get(category, 0) + cost.amount

    # Przygotowanie danych do wykresu
    labels = list(summary.keys())
    data = list(summary.values())

    return render_template(
        'cost_summary.html',
        summary=summary,
        selected_year=selected_year,
        selected_month=selected_month,
        labels=labels,
        data=data
    )


    # Grupowanie kosztów według kategorii dla wybranego miesiąca
    costs = Cost.query.filter(Cost.date.startswith(selected_year_month)).all()
    summary = {}
    for cost in costs:
        category = cost.category
        summary[category] = summary.get(category, 0) + cost.amount

    # Przygotowanie danych do wykresu
    labels = list(summary.keys())
    data = list(summary.values())

    return render_template(
        'cost_summary.html',
        summary=summary,
        selected_year=selected_year,
        selected_month=selected_month,
        labels=labels,
        data=data
    )
):
    # Pobranie parametrów month i year z GET (domyślnie bieżący miesiąc i rok)
    today = date.today()
    current_year = today.year
    current_month = today.month

    selected_year = request.args.get('year', current_year, type=int)
    selected_month = request.args.get('month', current_month, type=int)
    
    # Sformatuj wybrany rok i miesiąc
    selected_year_month = f"{selected_year}-{selected_month:02d}"

    # Grupowanie kosztów według kategorii dla wybranego miesiąca
    costs = Cost.query.filter(Cost.date.startswith(selected_year_month)).all()
    summary = {}
    for cost in costs:
        category = cost.category
        summary[category] = summary.get(category, 0) + cost.amount

    return render_template(
        'cost_summary.html',
        summary=summary,
        selected_year=selected_year,
        selected_month=selected_month
    )
