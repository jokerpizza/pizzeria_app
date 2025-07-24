import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///rentownosc.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Ingredient, Recipe, RecipeIngredient

@app.before_first_request
def create_tables():
    db.create_all()

# Ingredient CRUD
@app.route('/api/ingredients', methods=['GET', 'POST'])
def handle_ingredients():
    if request.method == 'GET':
        items = Ingredient.query.all()
        return jsonify([i.to_dict() for i in items])
    data = request.json
    ing = Ingredient(
        name=data['name'],
        base_quantity=data['base_quantity'],
        unit=data['unit'],
        price_for_base=data['price_for_base']
    )
    db.session.add(ing)
    db.session.commit()
    return jsonify(ing.to_dict()), 201

# Recipe CRUD
@app.route('/api/recipes', methods=['GET', 'POST'])
def handle_recipes():
    if request.method == 'GET':
        recipes = Recipe.query.all()
        return jsonify([r.to_dict() for r in recipes])
    data = request.json
    rec = Recipe(
        name=data['name'],
        category=data['category'],
        price_dine_in=data['price_dine_in'],
        price_delivery=data['price_delivery'],
        trade_names=",".join(data.get('trade_names', []))
    )
    db.session.add(rec)
    db.session.commit()
    # add ingredients
    for item in data.get('ingredients', []):
        link = RecipeIngredient(
            recipe_id=rec.id,
            ingredient_id=item['ingredient_id'],
            quantity=item['quantity']
        )
        db.session.add(link)
    db.session.commit()
    return jsonify(rec.to_dict()), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))