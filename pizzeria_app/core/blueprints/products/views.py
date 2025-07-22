from flask import render_template, redirect, url_for, flash, request
from .forms import ProductForm, PriceForm
from . import products_bp
from ...extensions import db
from ...models import Product, ProductPrice

def _commit():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def login_dummy(f):
    # placeholder decorator if later you add login
    return f

@products_bp.route("/list")
@login_dummy
def products_list():
    products = Product.query.order_by(Product.name).all()
    return render_template("products/list.html", products=products)

@products_bp.route("/new", methods=["GET","POST"])
@login_dummy
def product_new():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(name=form.name.data.strip(), unit=form.unit.data)
        db.session.add(p)
        _commit()
        flash("Produkt dodany", "success")
        return redirect(url_for("products.products_list"))
    return render_template("products/new.html", form=form)

@products_bp.route("/prices")
@login_dummy
def prices_list():
    prices = ProductPrice.query.order_by(ProductPrice.valid_from.desc()).all()
    return render_template("products/prices.html", prices=prices)

@products_bp.route("/prices/new", methods=["GET","POST"])
@login_dummy
def price_new():
    form = PriceForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.order_by(Product.name)]
    if form.validate_on_submit():
        pp = ProductPrice(
            product_id=form.product_id.data,
            price=form.price.data,
            quantity=form.quantity.data,
            currency=form.currency.data.upper(),
            valid_from=form.valid_from.data
        )
        db.session.add(pp)
        _commit()
        flash("Cena dodana", "success")
        return redirect(url_for("products.prices_list"))
    return render_template("products/price_new.html", form=form)
