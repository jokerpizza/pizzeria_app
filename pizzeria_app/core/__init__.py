import os
from flask import Flask, render_template
from .extensions import db, migrate
from .models import ensure_tables
from .blueprints.products import products_bp

def create_app():
    app = Flask(__name__)
    # basic config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://","postgresql://",1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # blueprints
    app.register_blueprint(products_bp, url_prefix="/products")

    @app.route("/")
    def index():
        return render_template("dashboard.html")

    # ensure tables exist if migrations not run
    with app.app_context():
        ensure_tables()

    return app
