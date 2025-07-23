from sqlalchemy.orm import Session
from . import models, schemas
from .utils import to_kg

# -------- settings (simple: env in runtime; no table needed) --------
import os
def get_fc_threshold()->float:
    try:
        return float(os.getenv("FC_THRESHOLD", "35"))
    except:
        return 35.0

# ------------- categories -------------
def create_prod_cat(db:Session, data:schemas.ProdCatCreate):
    obj=models.ProductCategory(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj
def list_prod_cat(db:Session): return db.query(models.ProductCategory).order_by(models.ProductCategory.name).all()

def create_rec_cat(db:Session, data:schemas.RecCatCreate):
    obj=models.RecipeCategory(**data.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj
def list_rec_cat(db:Session): return db.query(models.RecipeCategory).order_by(models.RecipeCategory.name).all()

# ------------- products -------------
def create_product(db:Session, data:schemas.ProductCreate):
    obj=models.Product(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj); return obj

def list_products(db:Session):
    q=db.query(models.Product).outerjoin(models.ProductCategory)
    return q.order_by(models.Product.name).all()

def get_product(db:Session, pid:int): return db.get(models.Product,pid)

def update_product(db:Session, pid:int, data:schemas.ProductUpdate):
    obj=get_product(db,pid)
    for k,v in data.model_dump().items(): setattr(obj,k,v)
    db.commit(); db.refresh(obj); return obj

def delete_product(db:Session, pid:int):
    obj=get_product(db,pid); db.delete(obj); db.commit()

# ------------- recipes -------------
def create_recipe(db:Session, data:schemas.RecipeCreate):
    r=models.Recipe(
        name=data.name,
        sale_price=data.sale_price,
        is_semi=data.is_semi,
        category_id=data.category_id
    )
    db.add(r); db.flush()
    for it in data.items:
        db.add(models.RecipeItem(recipe_id=r.id, **it.model_dump()))
    db.commit(); db.refresh(r); return r

def get_recipe(db:Session, rid:int): return db.get(models.Recipe,rid)

def update_recipe(db:Session, rid:int, data:schemas.RecipeUpdate):
    r=get_recipe(db,rid)
    r.name=data.name; r.sale_price=data.sale_price; r.is_semi=data.is_semi; r.category_id=data.category_id
    db.query(models.RecipeItem).filter(models.RecipeItem.recipe_id==rid).delete()
    for it in data.items:
        db.add(models.RecipeItem(recipe_id=rid, **it.model_dump()))
    db.commit(); db.refresh(r); return r

def delete_recipe(db:Session, rid:int):
    r=get_recipe(db,rid); db.delete(r); db.commit()

def list_recipes(db:Session):
    return db.query(models.Recipe).order_by(models.Recipe.name).all()

def compute_recipe_totals(recipe: models.Recipe, threshold: float):
    # recursion
    cost=0.0
    for it in recipe.items:
        if it.product_id:
            cost += it.product.price_per_kg * to_kg(it.amount, it.unit)
        else:
            # semi recipe cost
            semi_cost,_,_,_ = compute_recipe_totals(it.semi, threshold)
            # treat amount as multiplier
            cost += semi_cost * it.amount
    sale = recipe.sale_price or 0
    fc = round(cost/sale*100,2) if sale else 0
    margin = round(sale - cost,2) if sale else 0
    cost = round(cost,2)
    alert = sale>0 and fc>threshold
    return cost, fc, margin, alert

def recipe_to_out(r, totals):
    cost, fc, margin, alert = totals
    items=[]
    for it in r.items:
        items.append({
            "id": it.id,
            "product_id": it.product_id,
            "semi_id": it.semi_id,
            "product_name": it.product.name if it.product_id else None,
            "semi_name": it.semi.name if it.semi_id else None,
            "amount": it.amount,
            "unit": it.unit
        })
    return {
        "id": r.id,
        "name": r.name,
        "sale_price": r.sale_price,
        "is_semi": r.is_semi,
        "category_id": r.category_id,
        "category_name": r.category.name if r.category else None,
        "items": items,
        "cost": cost,
        "food_cost_pct": fc,
        "margin": margin,
        "alert": alert
    }
