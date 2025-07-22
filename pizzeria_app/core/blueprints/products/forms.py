from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

UNITS = [('szt','szt'),('kg','kg'),('g','g'),('l','l'),('ml','ml')]

class ProductForm(FlaskForm):
    name = StringField("Nazwa", validators=[DataRequired(), Length(max=120)])
    unit = SelectField("Jednostka", choices=UNITS, validators=[DataRequired()])
    submit = SubmitField("Zapisz")

class PriceForm(FlaskForm):
    product_id = SelectField("Produkt", coerce=int, validators=[DataRequired()])
    quantity = FloatField("Ilość w opakowaniu", validators=[DataRequired(), NumberRange(min=0.0001)])
    price = DecimalField("Cena opakowania", places=2, rounding=None, validators=[DataRequired(), NumberRange(min=0)])
    currency = StringField("Waluta", default="PLN", validators=[Length(max=4)])
    submit = SubmitField("Zapisz")
