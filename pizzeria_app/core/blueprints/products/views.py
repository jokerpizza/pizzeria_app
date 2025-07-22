from flask import render_template, request, redirect, url_for, flash
from . import products_bp
from .forms import ProductForm, PriceForm
from ...extensions import db
from ...models import Product, ProductPrice
from datetime import datetime

def _commit():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

@products_bp.route('/list')
def list_products():
    products = Product.query.order_by(Product.name).all()
    return render_template('products/list.html', products=products)

@products_bp.route('/new', methods=['GET','POST'])
def product_new():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(name=form.name.data,
                    unit=form.unit.data,
                    price_per_unit=form.price_per_unit.data)
        db.session.add(p)
        _commit()
        flash('Dodano produkt', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/new.html', form=form)

@products_bp.route('/prices')
def prices():
    prices = ProductPrice.query.join(Product).add_columns(Product.name, ProductPrice.price, ProductPrice.valid_from).order_by(Product.name).all()
    return render_template('products/prices.html', prices=prices)

@products_bp.route('/prices/new', methods=['GET','POST'])
def price_new():
    form = PriceForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.order_by(Product.name)]
    if form.validate_on_submit():
        pr = ProductPrice(product_id=form.product_id.data,
                          price=form.price.data,
                          valid_from=form.valid_from.data)
        db.session.add(pr)
        _commit()
        flash('Dodano cenę', 'success')
        return redirect(url_for('products.prices'))
    return render_template('products/price_new.html', form=form)
