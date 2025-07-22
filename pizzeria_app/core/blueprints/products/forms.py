from wtforms import StringField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

UNITS = [('szt','szt'),('kg','kg'),('l','l')]

class ProductForm(FlaskForm):
    name = StringField('Nazwa', validators=[DataRequired()])
    unit = SelectField('Jednostka', choices=UNITS, validators=[DataRequired()])
    price_per_unit = DecimalField('Cena zakupu / jednostkę', places=2, validators=[DataRequired()])

class PriceForm(FlaskForm):
    product_id = SelectField('Produkt', coerce=int, validators=[DataRequired()])
    price = DecimalField('Cena zakupu / jednostkę', places=2, validators=[DataRequired()])
    valid_from = DateField('Obowiązuje od', validators=[DataRequired()])
