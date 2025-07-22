from flask import Blueprint
products_bp = Blueprint('products', __name__, template_folder='../../templates/products')
from . import views
