from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models
from app.schemas.schemas import MappingBase, MappingRead
from typing import List

router = APIRouter()

@router.get("/", response_model=List[MappingRead])
def list_mappings(db: Session = Depends(get_db)):
    return db.query(models.NameMapping).all()

@router.post("/", response_model=MappingRead)
def create_mapping(payload: MappingBase, db: Session = Depends(get_db)):
    m=models.NameMapping(**payload.dict())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.put("/{mapping_id}", response_model=MappingRead)
def update_mapping(mapping_id: int, mapping: MappingBase, db: Session = Depends(get_db)):
    db_item = db.query(NameMapping).filter(NameMapping.id == mapping_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Mapping not found")
    db_item.external_name = mapping.external_name
    db_item.recipe_id = mapping.recipe_id
    db.commit()
    db.refresh(db_item)
    return db_item
