from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from .. import models, schemas

router = APIRouter()

@router.get('', response_model=list[schemas.RecipeRead])
def list_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).all()

@router.post('', response_model=schemas.RecipeRead)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = models.Recipe(name=recipe.name, sale_price=recipe.sale_price, category=recipe.category)
    db.add(db_recipe)
    db.commit()
    for item in recipe.items:
        db_item = models.RecipeItem(recipe_id=db_recipe.id, ingredient_id=item.ingredient_id, quantity=item.quantity)
        db.add(db_item)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe