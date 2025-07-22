from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[schemas.ProductOut])
def list_(db:Session=Depends(get_db)):
    res=[]
    for p in crud.list_products(db):
        d = schemas.ProductOut.from_orm(p).dict()
        d['category_name']= p.category.name if p.category else None
        res.append(d)
    return res

@router.post("/", response_model=schemas.ProductOut)
def create(data:schemas.ProductCreate, db:Session=Depends(get_db)):
    return schemas.ProductOut.from_orm(crud.create_product(db,data))

@router.put("/{pid}", response_model=schemas.ProductOut)
def update(pid:int, data:schemas.ProductUpdate, db:Session=Depends(get_db)):
    if not crud.get_product(db,pid): raise HTTPException(404)
    return schemas.ProductOut.from_orm(crud.update_product(db,pid,data))

@router.delete("/{pid}")
def delete(pid:int, db:Session=Depends(get_db)):
    if not crud.get_product(db,pid): raise HTTPException(404)
    crud.delete_product(db,pid); return {"ok":True}
