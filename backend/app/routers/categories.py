from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..deps import get_db

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)

@router.post("/", response_model=schemas.CategoryOut, status_code=201)
def create_category(data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, data)

@router.put("/{cat_id}", response_model=schemas.CategoryOut)
def update_category(cat_id: int, data: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    obj = crud.update_category(db, cat_id, data)
    if not obj:
        raise HTTPException(404, "Category not found")
    return obj

@router.delete("/{cat_id}", status_code=204)
def delete_category(cat_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_category(db, cat_id)
    if not ok:
        raise HTTPException(404, "Category not found")
