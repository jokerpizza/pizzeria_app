import os
from flask import Flask, render_template
from .extensions import db, migrate
from .blueprints.products import products_bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://","postgresql://",1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(products_bp, url_prefix="/products")

    @app.route("/")
    def index():
        return render_template("dashboard.html")

    return app
