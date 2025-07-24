from app import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    base_quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(16), nullable=False)
    price_for_base = db.Column(db.Float, nullable=False)

    def to_dict(self):
        price_per_unit = self.price_for_base / self.base_quantity if self.base_quantity else 0
        return {
            'id': self.id,
            'name': self.name,
            'base_quantity': self.base_quantity,
            'unit': self.unit,
            'price_for_base': self.price_for_base,
            'price_per_unit': price_per_unit
        }

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    price_dine_in = db.Column(db.Float, nullable=False)
    price_delivery = db.Column(db.Float, nullable=False)
    trade_names = db.Column(db.String(256), nullable=True)
    ingredients = db.relationship('RecipeIngredient', backref='recipe', cascade="all, delete-orphan")

    def to_dict(self):
        total_cost = sum(ri.ingredient.price_for_base / ri.ingredient.base_quantity * ri.quantity for ri in self.ingredients)
        fc_dine = (total_cost / self.price_dine_in * 100) if self.price_dine_in else 0
        fc_del = (total_cost / self.price_delivery * 100) if self.price_delivery else 0
        margin_pln_dine = self.price_dine_in - total_cost
        margin_pln_del = self.price_delivery - total_cost
        margin_pct_dine = (margin_pln_dine / self.price_dine_in * 100) if self.price_dine_in else 0
        margin_pct_del = (margin_pln_del / self.price_delivery * 100) if self.price_delivery else 0
        markup_pct = ((self.price_dine_in - total_cost) / total_cost * 100) if total_cost else 0
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price_dine_in': self.price_dine_in,
            'price_delivery': self.price_delivery,
            'trade_names': self.trade_names.split(',') if self.trade_names else [],
            'ingredients': [ri.to_dict() for ri in self.ingredients],
            'food_cost_dine_in_pct': fc_dine,
            'food_cost_delivery_pct': fc_del,
            'margin_pln_dine': margin_pln_dine,
            'margin_pln_delivery': margin_pln_del,
            'margin_pct_dine': margin_pct_dine,
            'margin_pct_delivery': margin_pct_del,
            'markup_pct': markup_pct
        }

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    ingredient = db.relationship('Ingredient')
    def to_dict(self):
        return {
            'id': self.id,
            'ingredient': self.ingredient.to_dict(),
            'quantity': self.quantity
        }