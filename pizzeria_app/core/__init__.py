import os
from flask import Flask, render_template
from .extensions import db, migrate
from .blueprints.products.views import products_bp

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///cost_core.db')
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://','postgresql://',1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def index():
        return render_template("dashboard.html")

    app.register_blueprint(products_bp, url_prefix="/products")
    return app
