from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

UNITS = [('szt','szt'), ('kg','kg'), ('g','g'), ('l','l'), ('ml','ml')]

class ProductForm(FlaskForm):
    name = StringField('Nazwa', validators=[DataRequired(), Length(max=120)])
    unit = SelectField('Jednostka', choices=UNITS, validators=[DataRequired()])
    submit = SubmitField('Zapisz')

class PriceForm(FlaskForm):
    product_id = SelectField('Produkt', coerce=int, validators=[DataRequired()])
    price_per_unit = DecimalField('Cena za jednostkę', validators=[DataRequired(), NumberRange(min=0)])
    valid_from = DateField('Ważna od', validators=[DataRequired()])
    submit = SubmitField('Zapisz')
