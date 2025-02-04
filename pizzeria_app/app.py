
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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

    try:
        sales = Sale.query.all()
        costs = Cost.query.all()

        labels = [s.date.strftime("%Y-%m-%d") for s in sales] if sales else []
        sales_data = [s.gotowka for s in sales] if sales else []
        cost_data = [c.amount for c in costs] if costs else []

        return render_template(
            'dashboard.html',
            labels=labels,
            sales_data=sales_data,
            cost_data=cost_data
        )
    except Exception as e:
        app.logger.error(f"Błąd ładowania dashboardu: {str(e)}")
        flash("Błąd serwera. Spróbuj ponownie później.", "danger")
        return redirect(url_for('index'))

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

if __name__ == "__main__":
    app.run(debug=True)
