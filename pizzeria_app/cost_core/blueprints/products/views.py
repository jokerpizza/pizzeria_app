from flask import render_template, redirect, url_for, flash
from flask import request
from .forms import ProductForm, PriceForm
from ...extensions import db
from ...models import Product, ProductPrice
from sqlalchemy import desc

# Dummy auth decorator (replace with your system later)
def login_required(f):
    from functools import wraps
    from flask import session, redirect, url_for, request
    @wraps(f)
    def wrapper(*args, **kwargs):
        # if 'user_id' not in session: return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return wrapper

@products_bp.route("/")
@login_required
def dashboard():
    return redirect(url_for("products_bp.products_list"))

@products_bp.route("/list")
@login_required
def products_list():
    products = Product.query.order_by(Product.name).all()
    return render_template("products/products_list.html", products=products)

@products_bp.route("/new", methods=["GET","POST"])
@login_required
def product_new():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(name=form.name.data.strip(), unit=form.unit.data)
        db.session.add(p)
        db.session.commit()
        flash("Dodano produkt", "success")
        return redirect(url_for("products_bp.products_list"))
    return render_template("products/product_form.html", form=form, action="Dodaj produkt")

@products_bp.route("/<int:pid>/edit", methods=["GET","POST"])
@login_required
def product_edit(pid):
    p = Product.query.get_or_404(pid)
    form = ProductForm(obj=p)
    if form.validate_on_submit():
        p.name = form.name.data.strip()
        p.unit = form.unit.data
        db.session.commit()
        flash("Zapisano", "success")
        return redirect(url_for("products_bp.products_list"))
    return render_template("products/product_form.html", form=form, action="Edytuj produkt")

@products_bp.route("/<int:pid>/delete", methods=["POST"])
@login_required
def product_delete(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash("Usunięto", "success")
    return redirect(url_for("products_bp.products_list"))

@products_bp.route("/prices")
@login_required
def prices_list():
    items = ProductPrice.query.order_by(desc(ProductPrice.valid_from)).all()
    return render_template("products/prices_list.html", items=items)

@products_bp.route("/prices/new", methods=["GET","POST"])
@login_required
def price_new():
    form = PriceForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.order_by(Product.name)]
    if form.validate_on_submit():
        unit_net = float(form.total_net.data) / float(form.quantity.data)
        price = ProductPrice(
            product_id=form.product_id.data,
            quantity=form.quantity.data,
            total_net=form.total_net.data,
            unit_net=unit_net,
            currency=form.currency.data.upper(),
            supplier=form.supplier.data.strip() if form.supplier.data else None,
            invoice_number=form.invoice_number.data.strip() if form.invoice_number.data else None
        )
        db.session.add(price)
        db.session.commit()
        flash("Dodano cenę", "success")
        return redirect(url_for("products_bp.prices_list"))
    return render_template("products/price_form.html", form=form, action="Dodaj cenę")

@products_bp.route("/prices/<int:iid>/edit", methods=["GET","POST"])
@login_required
def price_edit(iid):
    price = ProductPrice.query.get_or_404(iid)
    form = PriceForm(obj=price)
    form.product_id.choices = [(p.id, p.name) for p in Product.query.order_by(Product.name)]
    if form.validate_on_submit():
        price.product_id = form.product_id.data
        price.quantity = form.quantity.data
        price.total_net = form.total_net.data
        price.unit_net = float(form.total_net.data) / float(form.quantity.data)
        price.currency = form.currency.data.upper()
        price.supplier = form.supplier.data.strip() if form.supplier.data else None
        price.invoice_number = form.invoice_number.data.strip() if form.invoice_number.data else None
        db.session.commit()
        flash("Zapisano", "success")
        return redirect(url_for("products_bp.prices_list"))
    return render_template("products/price_form.html", form=form, action="Edytuj cenę")

@products_bp.route("/prices/<int:iid>/delete", methods=["POST"])
@login_required
def price_delete(iid):
    price = ProductPrice.query.get_or_404(iid)
    db.session.delete(price)
    db.session.commit()
    flash("Usunięto", "success")
    return redirect(url_for("products_bp.prices_list"))

@products_bp.route("/<int:pid>/history")
@login_required
def price_history(pid):
    product = Product.query.get_or_404(pid)
    history = product.prices.order_by(ProductPrice.valid_from.desc()).all()
    return render_template("products/price_history.html", product=product, history=history)
