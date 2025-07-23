from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from .. import models, schemas

router = APIRouter()

@router.get('', response_model=list[schemas.IngredientRead])
def list_ingredients(db: Session = Depends(get_db)):
    return db.query(models.Ingredient).all()

@router.post('', response_model=schemas.IngredientRead)
def create_ingredient(ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    db_ing = models.Ingredient(**ingredient.dict())
    db.add(db_ing)
    db.commit()
    db.refresh(db_ing)
    return db_ing