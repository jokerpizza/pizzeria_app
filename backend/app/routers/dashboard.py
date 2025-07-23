from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, crud, schemas

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_model=schemas.DashOut)
def dash(db:Session=Depends(get_db)):
    threshold = crud.get_fc_threshold()
    product_count = db.query(models.Product).count()
    recipes = db.query(models.Recipe).all()
    if recipes:
        fcs=[]
        data=[]
        alerts=[]
        for r in recipes:
            cost, fc, margin, alert = crud.compute_recipe_totals(r, threshold)
            fcs.append(fc)
            data.append((r.name, cost))
            if alert:
                alerts.append({"name": r.name, "fc": fc})
        avg_fc = round(sum(fcs)/len(fcs),2)
        top5 = sorted(data, key=lambda x:x[1], reverse=True)[:5]
    else:
        avg_fc=0; top5=[]; alerts=[]
    return schemas.DashOut(
        product_count=product_count,
        avg_food_cost_pct=avg_fc,
        top5_expensive=[{"name":n,"cost":c} for n,c in top5],
        alerts=alerts
    )
