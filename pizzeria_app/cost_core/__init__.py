from flask import Flask
from .config import Config
from .extensions import db, migrate
from .blueprints.products import products_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(products_bp, url_prefix="/products")

    @app.route("/")
    def index():
        from .models import ProductPrice
        from sqlalchemy import func
        data = []
        return render_template("dashboard.html")

    return app

app = create_app()
