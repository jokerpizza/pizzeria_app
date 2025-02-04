from flask import Flask
from models import db
from routes.safe import safe_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pizzeria.db"
db.init_app(app)

app.register_blueprint(safe_bp, url_prefix="/safe")  # Dodano url_prefix

if __name__ == "__main__":
    app.run(debug=True)
