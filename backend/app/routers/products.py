from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..deps import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    return crud.list_products(db)

@router.post("/", response_model=schemas.ProductOut, status_code=201)
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db)):
    if crud.get_product_by_name(db, data.name):
        raise HTTPException(400, "Product with this name already exists")
    return crud.create_product(db, data)

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    obj = crud.update_product(db, product_id, data)
    if not obj:
        raise HTTPException(404, "Product not found")
    return obj

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_product(db, product_id)
    if not ok:
        raise HTTPException(404, "Product not found")
