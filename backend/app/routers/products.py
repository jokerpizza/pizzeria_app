from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=schemas.ProductOut)
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, data)

@router.get("/", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    return crud.list_products(db)

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    if not crud.get_product(db, product_id):
        raise HTTPException(404)
    return crud.update_product(db, product_id, data)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not crud.get_product(db, product_id):
        raise HTTPException(404)
    crud.delete_product(db, product_id)
    return {"ok": True}
