from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/products", response_model=list[schemas.ProdCatOut])
def list_prod(db:Session=Depends(get_db)):
    return [schemas.ProdCatOut.from_orm(c) for c in crud.list_prod_cat(db)]

@router.post("/products", response_model=schemas.ProdCatOut)
def create_prod(data:schemas.ProdCatCreate, db:Session=Depends(get_db)):
    return schemas.ProdCatOut.from_orm(crud.create_prod_cat(db,data))

@router.get("/recipes", response_model=list[schemas.RecCatOut])
def list_rec(db:Session=Depends(get_db)):
    return [schemas.RecCatOut.from_orm(c) for c in crud.list_rec_cat(db)]

@router.post("/recipes", response_model=schemas.RecCatOut)
def create_rec(data:schemas.RecCatCreate, db:Session=Depends(get_db)):
    return schemas.RecCatOut.from_orm(crud.create_rec_cat(db,data))
