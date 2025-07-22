from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired, Length, NumberRange

UNITS = [("szt","szt"),("kg","kg"),("l","l"),("g","g"),("ml","ml")]

class ProductForm(FlaskForm):
    name = StringField("Nazwa", validators=[DataRequired(), Length(max=120)])
    unit = SelectField("Jednostka", choices=UNITS, validators=[DataRequired()])

class PriceForm(FlaskForm):
    product_id = SelectField("Produkt", coerce=int, validators=[DataRequired()])
    price = DecimalField("Cena", validators=[DataRequired(), NumberRange(min=0)])
    quantity = DecimalField("Ilość", validators=[DataRequired(), NumberRange(min=0.0001)])
    currency = StringField("Waluta", default="PLN", validators=[DataRequired(), Length(max=3)])
    valid_from = DateField("Od dnia", format="%Y-%m-%d")
