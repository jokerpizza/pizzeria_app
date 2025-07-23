from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models
from app.schemas.schemas import OrderRead
from typing import List

router = APIRouter()

@router.get("/", response_model=List[OrderRead])
def list_orders(limit:int=100, db: Session = Depends(get_db)):
    return db.query(models.Order).order_by(models.Order.id.desc()).limit(limit).all()

@router.put("/{order_id}", response_model=OrderRead)
def update_order(order_id: int, order_data: OrderRead, db: Session = Depends(get_db)):
    db_item = db.query(Order).filter(Order.id == order_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Order not found")
    db_item.vendor = order_data.vendor
    db_item.created_at = order_data.created_at
    db.commit()
    db.refresh(db_item)
    return db_item
