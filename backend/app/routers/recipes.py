from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud, models

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/", response_model=list[schemas.RecipeOut])
def list_(db:Session=Depends(get_db),
          sort: str = Query("name"),
          order: str = Query("asc"),
          only_semi: bool = False,
          alert_only: bool = False,
          margin_lt: float | None = None,
          fc_gt: float | None = None):
    threshold = crud.get_fc_threshold()
    res=[]
    recipes = crud.list_recipes(db)
    # filters
    if only_semi:
        recipes=[r for r in recipes if r.is_semi]
    out=[]
    for r in recipes:
        totals = crud.compute_recipe_totals(r, threshold)
        if alert_only and not totals[3]:
            continue
        if margin_lt is not None and not (totals[2] < margin_lt):
            continue
        if fc_gt is not None and not (totals[1] > fc_gt):
            continue
        out.append(crud.recipe_to_out(r, totals))
    # sort
    key_map = {
        "name": lambda x: x["name"],
        "margin": lambda x: x["margin"],
        "fc": lambda x: x["food_cost_pct"],
        "cost": lambda x: x["cost"]
    }
    key = key_map.get(sort, key_map["name"])
    out.sort(key=key, reverse=(order=="desc"))
    return out

@router.post("/", response_model=schemas.RecipeOut)
def create(data:schemas.RecipeCreate, db:Session=Depends(get_db)):
    r=crud.create_recipe(db,data)
    totals=crud.compute_recipe_totals(r, crud.get_fc_threshold())
    return crud.recipe_to_out(r, totals)

@router.put("/{rid}", response_model=schemas.RecipeOut)
def update(rid:int, data:schemas.RecipeUpdate, db:Session=Depends(get_db)):
    if not crud.get_recipe(db,rid): raise HTTPException(404)
    r=crud.update_recipe(db,rid,data)
    totals=crud.compute_recipe_totals(r, crud.get_fc_threshold())
    return crud.recipe_to_out(r, totals)

@router.get("/{rid}", response_model=schemas.RecipeOut)
def get_one(rid:int, db:Session=Depends(get_db)):
    r=crud.get_recipe(db,rid)
    if not r: raise HTTPException(404)
    totals=crud.compute_recipe_totals(r, crud.get_fc_threshold())
    return crud.recipe_to_out(r, totals)

@router.delete("/{rid}")
def delete(rid:int, db:Session=Depends(get_db)):
    if not crud.get_recipe(db,rid): raise HTTPException(404)
    crud.delete_recipe(db,rid); return {"ok":True}
