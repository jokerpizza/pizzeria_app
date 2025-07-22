
from flask import Blueprint, render_template, redirect, url_for, flash
from flask import request
from flask_login import login_required
from sqlalchemy import desc
from models import Product, ProductPrice, db
from wtforms import StringField, DecimalField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm

costs_rt_bp = Blueprint('rtcosts', __name__, template_folder='../../templates/realtime_costs')

class ProductForm(FlaskForm):
    name = StringField("Nazwa", validators=[DataRequired()])
    unit = SelectField("Jednostka", choices=[("kg","kg"),("l","l"),("szt","szt")], validators=[DataRequired()])

class ProductPriceForm(FlaskForm):
    product_id = SelectField("Produkt", coerce=int, validators=[DataRequired()])
    supplier = StringField("Dostawca")
    quantity = FloatField("Ilość", validators=[DataRequired(), NumberRange(min=0.0001)])
    total_net = DecimalField("Wartość netto", validators=[DataRequired(), NumberRange(min=0)])
    currency = StringField("Waluta", default="PLN")
    invoice_number = StringField("Faktura")

@costs_rt_bp.route('/products')
@login_required
def products_list():
    products = Product.query.order_by(Product.name).all()
    return render_template('realtime_costs/products_list.html', products=products)

@costs_rt_bp.route('/products/new', methods=['GET','POST'])
@login_required
def product_new():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(name=form.name.data.strip(), unit=form.unit.data)
        db.session.add(p)
        db.session.commit()
        flash('Produkt dodany', 'success')
        return redirect(url_for('rtcosts.products_list'))
    return render_template('realtime_costs/product_form.html', form=form, action='Dodaj produkt')

@costs_rt_bp.route('/products/<int:pid>/edit', methods=['GET','POST'])
@login_required
def product_edit(pid):
    p = Product.query.get_or_404(pid)
    form = ProductForm(obj=p)
    if form.validate_on_submit():
        p.name = form.name.data.strip()
        p.unit = form.unit.data
        db.session.commit()
        flash('Zapisano', 'success')
        return redirect(url_for('rtcosts.products_list'))
    return render_template('realtime_costs/product_form.html', form=form, action='Edytuj produkt')

@costs_rt_bp.route('/products/<int:pid>/delete', methods=['POST'])
@login_required
def product_delete(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash('Usunięto', 'success')
    return redirect(url_for('rtcosts.products_list'))

@costs_rt_bp.route('/purchases')
@login_required
def purchases_list():
    items = ProductPrice.query.order_by(desc(ProductPrice.valid_from)).all()
    return render_template('realtime_costs/purchases_list.html', items=items)

@costs_rt_bp.route('/purchases/new', methods=['GET','POST'])
@login_required
def purchase_new():
    form = ProductPriceForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.order_by(Product.name)]
    if form.validate_on_submit():
        unit_net = float(form.total_net.data) / float(form.quantity.data)
        item = ProductPrice(
            product_id=form.product_id.data,
            supplier=form.supplier.data.strip() if form.supplier.data else None,
            quantity=form.quantity.data,
            total_net=form.total_net.data,
            unit_net=unit_net,
            currency=form.currency.data.upper(),
            invoice_number=form.invoice_number.data.strip() if form.invoice_number.data else None,
        )
        db.session.add(item)
        db.session.commit()
        flash('Zakup dodany', 'success')
        return redirect(url_for('rtcosts.purchases_list'))
    return render_template('realtime_costs/purchase_form.html', form=form, action='Dodaj zakup')

@costs_rt_bp.route('/purchases/<int:iid>/edit', methods=['GET','POST'])
@login_required
def purchase_edit(iid):
    item = ProductPrice.query.get_or_404(iid)
    form = ProductPriceForm(obj=item)
    form.product_id.choices = [(p.id, p.name) for p in Product.query.order_by(Product.name)]
    if form.validate_on_submit():
        item.product_id = form.product_id.data
        item.supplier = form.supplier.data.strip() if form.supplier.data else None
        item.quantity = form.quantity.data
        item.total_net = form.total_net.data
        item.unit_net = float(form.total_net.data) / float(form.quantity.data)
        item.currency = form.currency.data.upper()
        item.invoice_number = form.invoice_number.data.strip() if form.invoice_number.data else None
        db.session.commit()
        flash('Zapisano', 'success')
        return redirect(url_for('rtcosts.purchases_list'))
    return render_template('realtime_costs/purchase_form.html', form=form, action='Edytuj zakup')

@costs_rt_bp.route('/purchases/<int:iid>/delete', methods=['POST'])
@login_required
def purchase_delete(iid):
    item = ProductPrice.query.get_or_404(iid)
    db.session.delete(item)
    db.session.commit()
    flash('Usunięto', 'success')
    return redirect(url_for('rtcosts.purchases_list'))

@costs_rt_bp.route('/products/<int:pid>/prices')
@login_required
def price_history(pid):
    p = Product.query.get_or_404(pid)
    history = p.price_entries.order_by(ProductPrice.valid_from.desc()).all()
    return render_template('realtime_costs/price_history.html', product=p, history=history)
