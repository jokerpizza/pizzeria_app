from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app import models
from app.schemas.schemas import MappingBase,MappingRead
from typing import List
from rapidfuzz.fuzz import ratio

router=APIRouter()

@router.get("/",response_model=List[MappingRead])
def list_mappings(unmapped:bool=False,db:Session=Depends(get_db)):
    q=db.query(models.NameMapping)
    return q.all()

@router.post("/",response_model=MappingRead)
def upsert_mapping(payload:MappingBase,db:Session=Depends(get_db)):
    m=db.query(models.NameMapping).filter_by(papu_name=payload.papu_name,papu_size=payload.papu_size).first()
    if m:
        m.recipe_id=payload.recipe_id
    else:
        m=models.NameMapping(**payload.dict())
        db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.delete("/{map_id}")
def delete_mapping(map_id:int,db:Session=Depends(get_db)):
    m=db.query(models.NameMapping).get(map_id)
    if not m: raise HTTPException(404)
    db.delete(m)
    db.commit()
    return {"ok":True}

@router.get("/suggest")
def suggest(name:str,size:str|None=None,limit:int=5,db:Session=Depends(get_db)):
    recs=db.query(models.Recipe).all()
    scored=[(r.id,ratio(name.lower(),r.name.lower())) for r in recs]
    scored.sort(key=lambda x:-x[1])
    return [{"recipe_id":rid,"score":sc} for rid,sc in scored[:limit]]
