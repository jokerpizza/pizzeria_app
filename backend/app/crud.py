from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

# Products
def create_product(db: Session, data: schemas.ProductCreate) -> models.Product:
    obj = models.Product(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_name(db: Session, name: str) -> Optional[models.Product]:
    return db.query(models.Product).filter(models.Product.name == name).first()

def list_products(db: Session) -> List[models.Product]:
    return db.query(models.Product).order_by(models.Product.name).all()

def update_product(db: Session, product_id: int, data: schemas.ProductUpdate) -> Optional[models.Product]:
    obj = get_product(db, product_id)
    if not obj:
        return None
    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_product(db: Session, product_id: int) -> bool:
    obj = get_product(db, product_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# Recipes
def create_recipe(db: Session, data: schemas.RecipeCreate) -> models.Recipe:
    recipe = models.Recipe(
        name=data.name,
        portion_size=data.portion_size,
        sale_price=data.sale_price,
    )
    db.add(recipe)
    db.flush()  # get recipe.id

    for item in data.items:
        db.add(models.RecipeItem(recipe_id=recipe.id, product_id=item.product_id, quantity=item.quantity))

    db.commit()
    db.refresh(recipe)
    return recipe

def get_recipe(db: Session, recipe_id: int) -> Optional[models.Recipe]:
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

def list_recipes(db: Session) -> List[models.Recipe]:
    return db.query(models.Recipe).order_by(models.Recipe.name).all()

def update_recipe(db: Session, recipe_id: int, data: schemas.RecipeUpdate) -> Optional[models.Recipe]:
    recipe = get_recipe(db, recipe_id)
    if not recipe:
        return None

    for k, v in data.dict(exclude_unset=True, exclude={'items'}).items():
        setattr(recipe, k, v)

    if data.items is not None:
        # replace items
        for it in list(recipe.items):
            db.delete(it)
        for item in data.items:
            db.add(models.RecipeItem(recipe_id=recipe.id, product_id=item.product_id, quantity=item.quantity))

    db.commit()
    db.refresh(recipe)
    return recipe

def delete_recipe(db: Session, recipe_id: int) -> bool:
    recipe = get_recipe(db, recipe_id)
    if not recipe:
        return False
    db.delete(recipe)
    db.commit()
    return True
