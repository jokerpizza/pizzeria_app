from flask import Flask, render_template, redirect, url_for, session
from models import db
from routes.safe import safe_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pizzeria.db"
app.secret_key = "supersecretkey"  # Klucz sesji
db.init_app(app)

# Rejestracja blueprintów
app.register_blueprint(safe_bp, url_prefix="/safe")

# Główna trasa aplikacji
@app.route("/")
def index():
    if "user_id" in session:
        return render_template("index.html")
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
