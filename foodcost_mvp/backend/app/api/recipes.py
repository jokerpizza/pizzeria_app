from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models
from app.schemas.schemas import RecipeCreate, RecipeRead
from typing import List

router = APIRouter()

@router.get("/", response_model=List[RecipeRead])
def list_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).all()

@router.post("/", response_model=RecipeRead)
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)):
    rec = models.Recipe(name=payload.name, sale_price=payload.sale_price, category=payload.category)
    db.add(rec)
    db.flush()
    for item in payload.items:
        db.add(models.RecipeItem(recipe_id=rec.id, ingredient_id=item.ingredient_id, quantity=item.quantity))
    db.commit()
    db.refresh(rec)
    return rec

@router.get("/{recipe_id}", response_model=RecipeRead)
def get_recipe(recipe_id:int, db: Session = Depends(get_db)):
    rec = db.query(models.Recipe).get(recipe_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Not found")
    return rec

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id:int, db: Session = Depends(get_db)):
    rec = db.query(models.Recipe).get(recipe_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(rec)
    db.commit()
    return {"ok":True}

@router.put("/{recipe_id}", response_model=RecipeRead)
def update_recipe(recipe_id: int, recipe_data: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db_recipe.name = recipe_data.name
    db.query(RecipeItem).filter(RecipeItem.recipe_id == recipe_id).delete()
    for item in recipe_data.items:
        db_item = RecipeItem(
            recipe_id=recipe_id,
            ingredient_id=item.ingredient_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe
