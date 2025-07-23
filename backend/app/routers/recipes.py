from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, models
from ..deps import get_db
from ..utils.calc import calc_food_cost, calc_food_cost_pct, calc_margin

router = APIRouter(prefix="/recipes", tags=["recipes"])

def recipe_to_out(recipe: models.Recipe) -> schemas.RecipeOut:
    # Convert model to schema with computed fields
    items_out = []
    for it in recipe.items:
        items_out.append(
            schemas.RecipeItemOut(
                id=it.id,
                product_id=it.product_id,
                quantity=it.quantity,
                product=schemas.ProductOut.from_orm(it.product)
            )
        )
    fc = calc_food_cost(items_out)
    return schemas.RecipeOut(
        id=recipe.id,
        name=recipe.name,
        portion_size=recipe.portion_size,
        sale_price=recipe.sale_price,
        items=items_out,
        food_cost=round(fc, 2),
        food_cost_pct=calc_food_cost_pct(fc, recipe.sale_price),
        margin=calc_margin(fc, recipe.sale_price)
    )

@router.get("/", response_model=List[schemas.RecipeOut])
def list_recipes(db: Session = Depends(get_db)):
    return [recipe_to_out(r) for r in crud.list_recipes(db)]

@router.post("/", response_model=schemas.RecipeOut, status_code=201)
def create_recipe(data: schemas.RecipeCreate, db: Session = Depends(get_db)):
    r = crud.create_recipe(db, data)
    return recipe_to_out(r)

@router.get("/{recipe_id}", response_model=schemas.RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    r = crud.get_recipe(db, recipe_id)
    if not r:
        raise HTTPException(404, "Recipe not found")
    return recipe_to_out(r)

@router.put("/{recipe_id}", response_model=schemas.RecipeOut)
def update_recipe(recipe_id: int, data: schemas.RecipeUpdate, db: Session = Depends(get_db)):
    r = crud.update_recipe(db, recipe_id, data)
    if not r:
        raise HTTPException(404, "Recipe not found")
    return recipe_to_out(r)

@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_recipe(db, recipe_id)
    if not ok:
        raise HTTPException(404, "Recipe not found")
