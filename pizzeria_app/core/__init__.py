from flask import Flask, render_template
from .extensions import db, migrate
from .blueprints.products import products_bp

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///data.db').replace('postgres://','postgresql://'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SECRET_KEY = os.getenv('SECRET_KEY','secret'),
    )
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(products_bp, url_prefix='/products')

    @app.route('/')
    def index():
        return render_template('dashboard.html')

    return app

import os
