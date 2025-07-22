from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..forms import ProductForm, PriceForm
from ...models import Product, ProductPrice
from ...extensions import db

def with_session(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        finally:
            db.session.remove()
    wrapper.__name__ = f.__name__
    return wrapper

products_bp = Blueprint("products", __name__, template_folder='../../templates/products')

@products_bp.route("/list")
@with_session
def products_list():
    products = Product.query.order_by(Product.name).all()
    return render_template("products/list.html", products=products)

@products_bp.route("/new", methods=["GET","POST"])
@with_session
def product_new():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(name=form.name.data, unit=form.unit.data)
        db.session.add(p)
        db.session.commit()
        flash("Produkt zapisany", "success")
        return redirect(url_for("products.products_list"))
    return render_template("products/new.html", form=form)

@products_bp.route("/prices")
@with_session
def prices_list():
    prices = ProductPrice.query.order_by(ProductPrice.valid_from.desc()).all()
    return render_template("products/prices_list.html", prices=prices)

@products_bp.route("/prices/new", methods=["GET","POST"])
@with_session
def price_new():
    form = PriceForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.order_by(Product.name)]
    if form.validate_on_submit():
        pr = ProductPrice(
            product_id=form.product_id.data,
            quantity=form.quantity.data,
            price=form.price.data,
            currency=form.currency.data or "PLN"
        )
        db.session.add(pr)
        db.session.commit()
        flash("Cena zapisana", "success")
        return redirect(url_for("products.prices_list"))
    return render_template("products/price_new.html", form=form)
