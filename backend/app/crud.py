from sqlalchemy.orm import Session
from . import models, schemas
from .utils.calc import convert_to_kg

def create_product(db: Session, data: schemas.ProductCreate):
    obj = models.Product(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_products(db: Session):
    return db.query(models.Product).order_by(models.Product.name).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).get(product_id)

def update_product(db: Session, product_id: int, data: schemas.ProductUpdate):
    obj = get_product(db, product_id)
    for k,v in data.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_product(db: Session, product_id: int):
    obj = get_product(db, product_id)
    db.delete(obj)
    db.commit()

# Recipes
def create_recipe(db: Session, data: schemas.RecipeCreate):
    recipe = models.Recipe(name=data.name, sale_price=data.sale_price)
    db.add(recipe)
    db.flush()
    for item in data.items:
        db.add(models.RecipeItem(recipe_id=recipe.id, **item.model_dump()))
    db.commit()
    db.refresh(recipe)
    return recipe

def update_recipe(db: Session, recipe_id: int, data: schemas.RecipeUpdate):
    recipe = db.query(models.Recipe).get(recipe_id)
    recipe.name = data.name
    recipe.sale_price = data.sale_price
    # replace items
    db.query(models.RecipeItem).filter(models.RecipeItem.recipe_id==recipe_id).delete()
    for item in data.items:
        db.add(models.RecipeItem(recipe_id=recipe_id, **item.model_dump()))
    db.commit()
    db.refresh(recipe)
    return recipe

def list_recipes(db: Session):
    return db.query(models.Recipe).order_by(models.Recipe.name).all()

def get_recipe(db: Session, recipe_id: int):
    return db.query(models.Recipe).get(recipe_id)

def delete_recipe(db: Session, recipe_id: int):
    r = get_recipe(db, recipe_id)
    db.delete(r)
    db.commit()

def compute_recipe_totals(recipe: models.Recipe):
    total_cost = 0.0
    for it in recipe.items:
        price_per_kg = it.product.price_per_kg
        kg_amount = convert_to_kg(it.amount, it.unit)
        total_cost += price_per_kg * kg_amount
    food_cost_pct = (total_cost / recipe.sale_price * 100) if recipe.sale_price else 0
    margin = recipe.sale_price - total_cost
    # round
    return round(total_cost,2), round(food_cost_pct,2), round(margin,2)
