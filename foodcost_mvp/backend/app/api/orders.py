from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.session import get_db
from .. import models
from ..schemas.schemas import OrderRead
from typing import List

router = APIRouter()

@router.get("/", response_model=List[OrderRead])
def list_orders(limit:int=100, db: Session = Depends(get_db)):
    return db.query(models.Order).order_by(models.Order.id.desc()).limit(limit).all()
