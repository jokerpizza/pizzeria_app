from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..crud import compute_recipe_totals

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
def dashboard(db: Session = Depends(get_db)):
    product_count = db.query(models.Product).count()
    recipes = db.query(models.Recipe).all()
    if recipes:
        fcs = []
        costs = []
        data = []
        for r in recipes:
            cost, fc, margin = compute_recipe_totals(r)
            fcs.append(fc)
            costs.append(cost)
            data.append((r.name, cost))
        avg_fc = round(sum(fcs)/len(fcs),2)
        top5 = sorted(data, key=lambda x: x[1], reverse=True)[:5]
    else:
        avg_fc = 0
        top5 = []

    return {
        "product_count": product_count,
        "avg_food_cost_pct": avg_fc,
        "top5_expensive": [{"name": n, "cost": c} for n,c in top5]
    }
