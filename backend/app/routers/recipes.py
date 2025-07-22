from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db
from ..crud import compute_recipe_totals

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.post("/", response_model=schemas.RecipeOut)
def create_recipe(data: schemas.RecipeCreate, db: Session = Depends(get_db)):
    r = crud.create_recipe(db, data)
    cost, fc, margin = compute_recipe_totals(r)
    return recipe_to_out(r, cost, fc, margin)

@router.get("/", response_model=list[schemas.RecipeOut])
def list_recipes(db: Session = Depends(get_db)):
    res = []
    for r in crud.list_recipes(db):
        cost, fc, margin = compute_recipe_totals(r)
        res.append(recipe_to_out(r, cost, fc, margin))
    return res

@router.get("/{recipe_id}", response_model=schemas.RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    r = crud.get_recipe(db, recipe_id)
    if not r:
        raise HTTPException(404)
    cost, fc, margin = compute_recipe_totals(r)
    return recipe_to_out(r, cost, fc, margin)

@router.put("/{recipe_id}", response_model=schemas.RecipeOut)
def update_recipe(recipe_id: int, data: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    if not crud.get_recipe(db, recipe_id):
        raise HTTPException(404)
    r = crud.update_recipe(db, recipe_id, data)
    cost, fc, margin = compute_recipe_totals(r)
    return recipe_to_out(r, cost, fc, margin)

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    if not crud.get_recipe(db, recipe_id):
        raise HTTPException(404)
    crud.delete_recipe(db, recipe_id)
    return {"ok": True}

def recipe_to_out(r, cost, fc, margin):
    items = []
    for it in r.items:
        items.append({
            "id": it.id,
            "product_id": it.product_id,
            "product_name": it.product.name,
            "amount": it.amount,
            "unit": it.unit
        })
    return {
        "id": r.id,
        "name": r.name,
        "sale_price": r.sale_price,
        "items": items,
        "cost": cost,
        "food_cost_pct": fc,
        "margin": margin
    }
