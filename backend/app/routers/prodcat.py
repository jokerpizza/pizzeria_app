from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..deps import get_db

router = APIRouter(prefix="/prodcat", tags=["prodcat"])

@router.get("/", response_model=List[schemas.ProdCatOut])
def list_all(db: Session = Depends(get_db)):
    items = []
    for pc in crud.list_prod_cat(db):
        items.append(schemas.ProdCatOut(
            id=pc.id,
            product_id=pc.product_id,
            category_id=pc.category_id,
            product=schemas.ProductOut.from_orm(pc.product),
            category=schemas.CategoryOut.from_orm(pc.category),
        ))
    return items

@router.post("/", response_model=schemas.ProdCatOut, status_code=201)
def create(data: schemas.ProdCatCreate, db: Session = Depends(get_db)):
    pc = crud.create_prod_cat(db, data)
    return schemas.ProdCatOut(
        id=pc.id,
        product_id=pc.product_id,
        category_id=pc.category_id,
        product=schemas.ProductOut.from_orm(pc.product),
        category=schemas.CategoryOut.from_orm(pc.category),
    )

@router.delete("/{pc_id}", status_code=204)
def delete(pc_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_prod_cat(db, pc_id)
    if not ok:
        raise HTTPException(404, "Not found")
