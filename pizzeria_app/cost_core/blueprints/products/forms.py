from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class ProductForm(FlaskForm):
    name = StringField("Nazwa", validators=[DataRequired()])
    unit = SelectField("Jednostka", choices=[("kg","kg"),("l","l"),("szt","szt")], validators=[DataRequired()])

class PriceForm(FlaskForm):
    product_id = SelectField("Produkt", coerce=int, validators=[DataRequired()])
    quantity = FloatField("Ilość", validators=[DataRequired(), NumberRange(min=0.0001)])
    total_net = DecimalField("Wartość netto", validators=[DataRequired(), NumberRange(min=0)])
    currency = StringField("Waluta", default="PLN")
    supplier = StringField("Dostawca")
    invoice_number = StringField("Faktura")
