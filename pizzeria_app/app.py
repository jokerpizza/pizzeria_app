
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, User, Sale, Cost, ATMDeposit

# Tworzenie instancji aplikacji Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

# Inicjalizacja bazy danych PRZED importowaniem modeli
db.init_app(app)

# Tworzenie bazy danych i konta administratora przy pierwszym uruchomieniu
with app.app_context():
    db.create_all()

    # Sprawdzenie, czy admin istnieje - jeśli nie, tworzymy go
    if not User.query.filter_by(username="admin").first():
        hashed_password = generate_password_hash("admin123", method="pbkdf2:sha256")
        admin_user = User(username="admin", password=hashed_password)
        db.session.add(admin_user)
        db.session.commit()
        print("🔹 Konto administratora utworzone: admin / admin123")

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                flash("Niepoprawne dane logowania", "danger")
        except Exception as e:
            app.logger.error(f"Błąd logowania: {str(e)}")
            flash("Błąd serwera. Spróbuj ponownie później.", "danger")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            if User.query.filter_by(username=username).first():
                flash("Użytkownik już istnieje", "danger")
            else:
                hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash("Rejestracja udana. Możesz się zalogować.", "success")
                return redirect(url_for('login'))
        except Exception as e:
            app.logger.error(f"Błąd rejestracji: {str(e)}")
            flash("Błąd serwera. Spróbuj ponownie później.", "danger")

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/safe', methods=['GET'])
def safe():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
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
    except Exception as e:
        app.logger.error(f"Błąd ładowania sejfu: {str(e)}")
        flash("Błąd serwera. Spróbuj ponownie później.", "danger")
        return redirect(url_for('dashboard'))

@app.route('/deposit-atm', methods=['POST'])
def deposit_atm():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        amount = request.form.get("amount")
        if amount:
            amount = float(amount)
            new_deposit = ATMDeposit(amount=amount, date=datetime.utcnow())
            db.session.add(new_deposit)
            db.session.commit()
        return redirect(url_for('safe'))
    except Exception as e:
        app.logger.error(f"Błąd wpłaty do sejfu: {str(e)}")
        flash("Błąd serwera. Spróbuj ponownie później.", "danger")
        return redirect(url_for('safe'))

if __name__ == "__main__":
    app.run(debug=True)
