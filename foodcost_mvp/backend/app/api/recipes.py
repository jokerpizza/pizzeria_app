from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from .. import models
from ..schemas.schemas import RecipeCreate, RecipeRead
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
