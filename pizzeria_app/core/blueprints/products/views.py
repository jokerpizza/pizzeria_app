from flask import Blueprint, render_template, redirect, url_for, flash, request
from ...extensions import db
from ...models import Product, ProductPrice
from .forms import ProductForm, PriceForm
from functools import wraps

products_bp = Blueprint('products', __name__, template_folder='templates')

def handle_db_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            db.session.rollback()
            flash(f'Błąd: {e}', 'danger')
            return redirect(request.referrer or url_for('products.products_list'))
    return wrapper

@products_bp.route("/list")
def products_list():
    products = Product.query.order_by(Product.name).all()
    return render_template("products/list.html", products=products)

@products_bp.route("/new", methods=['GET','POST'])
@handle_db_errors
def product_new():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(name=form.name.data, unit=form.unit.data)
        db.session.add(p)
        db.session.commit()
        flash("Produkt dodany.", "success")
        return redirect(url_for('products.products_list'))
    return render_template("products/new.html", form=form)

@products_bp.route("/prices")
def prices_list():
    prices = ProductPrice.query.order_by(ProductPrice.valid_from.desc()).all()
    return render_template("products/prices_list.html", prices=prices)

@products_bp.route("/prices/new", methods=['GET','POST'])
@handle_db_errors
def price_new():
    form = PriceForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.order_by(Product.name)]
    if form.validate_on_submit():
        pr = ProductPrice(product_id=form.product_id.data,
                          price_per_unit=form.price_per_unit.data,
                          valid_from=form.valid_from.data)
        db.session.add(pr)
        db.session.commit()
        flash("Cena dodana.", "success")
        return redirect(url_for('products.prices_list'))
    return render_template("products/price_new.html", form=form)
