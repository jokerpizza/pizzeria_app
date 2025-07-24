from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Ingredient, Recipe, RecipeIngredient
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app, db)

@app.route('/ingredients', methods=['GET', 'POST'])
def manage_ingredients():
    if request.method == 'POST':
        data = request.json
        ing = Ingredient(
            name=data['name'], unit=data['unit'], price_per_unit=data['price_per_unit']
        )
        db.session.add(ing)
        db.session.commit()
        return jsonify({'id': ing.id}), 201
    items = Ingredient.query.all()
    return jsonify([{'id': i.id, 'name': i.name, 'unit': i.unit, 'price_per_unit': i.price_per_unit} for i in items])

@app.route('/recipes', methods=['GET', 'POST'])
def manage_recipes():
    if request.method == 'POST':
        data = request.json
        rec = Recipe(
            name=data['name'], category=data['category'], 
            price_dine_in=data['price_dine_in'], price_delivery=data['price_delivery'],
            trade_names=data.get('trade_names', [])
        )
        db.session.add(rec)
        db.session.flush()
        for ri in data['ingredients']:
            assoc = RecipeIngredient(
                recipe_id=rec.id,
                ingredient_id=ri['ingredient_id'],
                quantity=ri['quantity']
            )
            db.session.add(assoc)
        db.session.commit()
        return jsonify({'id': rec.id}), 201
    recipes = []
    for r in Recipe.query.all():
        cost = sum(ri.quantity * ri.ingredient.price_per_unit for ri in r.ingredients)
        recipes.append({
            'id': r.id,
            'name': r.name,
            'category': r.category,
            'price_dine_in': r.price_dine_in,
            'price_delivery': r.price_delivery,
            'food_cost_dine_in': cost / r.price_dine_in * 100,
            'margin_dine_in': (r.price_dine_in - cost) / r.price_dine_in * 100,
            'markup_dine_in': (r.price_dine_in - cost) / cost * 100,
            'profit_pln_dine_in': r.price_dine_in - cost,
            'food_cost_delivery': cost / r.price_delivery * 100,
            'margin_delivery': (r.price_delivery - cost) / r.price_delivery * 100,
            'markup_delivery': (r.price_delivery - cost) / cost * 100,
            'profit_pln_delivery': r.price_delivery - cost,
        })
    return jsonify(recipes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
