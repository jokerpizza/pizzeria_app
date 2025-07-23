from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from typing import List, Optional
from . import models, schemas

# Products
def create_product(db: Session, data: schemas.ProductCreate) -> models.Product:
    obj = models.Product(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    return db.get(models.Product, product_id)

def get_product_by_name(db: Session, name: str) -> Optional[models.Product]:
    return db.scalar(select(models.Product).where(models.Product.name == name))

def list_products(db: Session) -> List[models.Product]:
    return db.scalars(select(models.Product).order_by(models.Product.name)).all()

def update_product(db: Session, product_id: int, data: schemas.ProductUpdate) -> Optional[models.Product]:
    obj = get_product(db, product_id)
    if not obj: return None
    for k,v in data.model_dump(exclude_unset=True).items():
        setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

def delete_product(db: Session, product_id: int) -> bool:
    obj = get_product(db, product_id)
    if not obj: return False
    db.delete(obj); db.commit(); return True

# Categories
def create_category(db: Session, data: schemas.CategoryCreate) -> models.Category:
    obj = models.Category(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj

def list_categories(db: Session) -> List[models.Category]:
    return db.scalars(select(models.Category).order_by(models.Category.name)).all()

def get_category(db: Session, cat_id: int) -> Optional[models.Category]:
    return db.get(models.Category, cat_id)

def update_category(db: Session, cat_id: int, data: schemas.CategoryUpdate) -> Optional[models.Category]:
    obj = get_category(db, cat_id)
    if not obj: return None
    for k,v in data.model_dump(exclude_unset=True).items():
        setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

def delete_category(db: Session, cat_id: int) -> bool:
    obj = get_category(db, cat_id)
    if not obj: return False
    db.delete(obj); db.commit(); return True

# ProdCat
def create_prod_cat(db: Session, data: schemas.ProdCatCreate) -> models.ProdCat:
    obj = models.ProdCat(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj

def list_prod_cat(db: Session) -> List[models.ProdCat]:
    return db.scalars(select(models.ProdCat)).all()

def delete_prod_cat(db: Session, pc_id: int) -> bool:
    obj = db.get(models.ProdCat, pc_id)
    if not obj: return False
    db.delete(obj); db.commit(); return True

# Recipes
def create_recipe(db: Session, data: schemas.RecipeCreate) -> models.Recipe:
    recipe = models.Recipe(name=data.name, portion_size=data.portion_size, sale_price=data.sale_price)
    db.add(recipe); db.flush()
    for item in data.items:
        db.add(models.RecipeItem(recipe_id=recipe.id, product_id=item.product_id, quantity=item.quantity))
    db.commit(); db.refresh(recipe); return recipe

def get_recipe(db: Session, recipe_id: int) -> Optional[models.Recipe]:
    return db.get(models.Recipe, recipe_id)

def list_recipes(db: Session) -> List[models.Recipe]:
    return db.scalars(select(models.Recipe).order_by(models.Recipe.name)).all()

def update_recipe(db: Session, recipe_id: int, data: schemas.RecipeUpdate) -> Optional[models.Recipe]:
    recipe = get_recipe(db, recipe_id)
    if not recipe: return None
    for k,v in data.model_dump(exclude_unset=True, exclude={'items'}).items():
        setattr(recipe,k,v)
    if data.items is not None:
        db.execute(delete(models.RecipeItem).where(models.RecipeItem.recipe_id==recipe.id))
        for item in data.items:
            db.add(models.RecipeItem(recipe_id=recipe.id, product_id=item.product_id, quantity=item.quantity))
    db.commit(); db.refresh(recipe); return recipe

def delete_recipe(db: Session, recipe_id: int) -> bool:
    recipe = get_recipe(db, recipe_id)
    if not recipe: return False
    db.delete(recipe); db.commit(); return True
