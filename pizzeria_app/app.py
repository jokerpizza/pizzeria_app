
from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Sale, Cost, RolePermissions
from functools import wraps

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
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/safe', methods=['GET'])
@login_required
def safe():
    total_cash_in = db.session.query(db.func.sum(Sale.dine_in)).scalar() or 0
    total_cash_out = db.session.query(db.func.sum(Cost.amount)).filter(Cost.payment_method == 'Gotówka').scalar() or 0
    current_cash = total_cash_in - total_cash_out

    recent_sales = Sale.query.order_by(Sale.date.desc()).limit(5).all()
    recent_costs = Cost.query.filter(Cost.payment_method == 'Gotówka').order_by(Cost.date.desc()).limit(5).all()

    recent_operations = [
        {"date": s.date, "type": "Wpływ", "amount": s.dine_in} for s in recent_sales
    ] + [
        {"date": c.date, "type": "Wypływ", "amount": c.amount} for c in recent_costs
    ]
    recent_operations = sorted(recent_operations, key=lambda x: x["date"], reverse=True)

    return render_template("safe.html", current_cash=current_cash, recent_operations=recent_operations)
