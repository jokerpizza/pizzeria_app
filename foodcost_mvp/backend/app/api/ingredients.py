from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models
from app.schemas.schemas import IngredientCreate, IngredientRead
from typing import List

router = APIRouter()

@router.get("/", response_model=List[IngredientRead])
def list_ingredients(db: Session = Depends(get_db)):
    return db.query(models.Ingredient).all()

@router.post("/", response_model=IngredientRead)
def create_ingredient(payload: IngredientCreate, db: Session = Depends(get_db)):
    ing = models.Ingredient(**payload.dict())
    db.add(ing)
    db.commit()
    db.refresh(ing)
    return ing

@router.put("/{ingredient_id}", response_model=IngredientRead)
def update_ingredient(ingredient_id:int, payload: IngredientCreate, db: Session = Depends(get_db)):
    ing = db.query(models.Ingredient).get(ingredient_id)
    if not ing:
        raise HTTPException(status_code=404, detail="Not found")
    for k,v in payload.dict().items():
        setattr(ing,k,v)
    db.commit()
    db.refresh(ing)
    return ing

@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id:int, db: Session = Depends(get_db)):
    ing = db.query(models.Ingredient).get(ingredient_id)
    if not ing:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(ing)
    db.commit()
    return {"ok":True}
