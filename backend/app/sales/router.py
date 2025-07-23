
from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .models_sales import OrderItem, Order
from ..crud import compute_recipe_totals

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/live")
def sales_live(hours: int = 24, db: Session = Depends(get_db)):
    """Return aggregated sales for last `hours`."""
    since = datetime.utcnow() - timedelta(hours=hours)
    items = db.query(OrderItem).join(Order).filter(Order.finished_at >= since).all()

    summary = {}
    for it in items:
        key = it.meal_name
        if key not in summary:
            summary[key] = {"qty": 0, "revenue": 0.0, "cost": 0.0, "margin": 0.0}
        summary[key]["qty"] += it.qty
        summary[key]["revenue"] += it.price_unit * it.qty
        summary[key]["cost"] += it.cost_unit * it.qty
        summary[key]["margin"] += it.margin_unit * it.qty

    # convert to list sorted by revenue desc
    report = [
        {
            "meal": k,
            **v,
            "food_cost_pct": round(v["cost"]/v["revenue"]*100,2) if v["revenue"] else 0
        }
        for k,v in sorted(summary.items(), key=lambda x: x[1]["revenue"], reverse=True)
    ]
    totals = {
        "qty": sum(v["qty"] for v in report),
        "revenue": round(sum(v["revenue"] for v in report),2),
        "cost": round(sum(v["cost"] for v in report),2),
        "margin": round(sum(v["margin"] for v in report),2),
        "food_cost_pct": round(sum(v["cost"] for v in report)/sum(v["revenue"] for v in report)*100,2) if report else 0
    }
    return {"since": since.isoformat(), "items": report, "totals": totals}

@router.get("/aliases/unmapped")
def unmapped_aliases(db: Session = Depends(get_db)):
    from .models_sales import OrderAlias
    rows = db.query(OrderAlias).filter(OrderAlias.recipe_id == None).all()
    return [{"id": r.id, "papu_name": r.papu_name} for r in rows]

@router.post("/aliases/{alias_id}/map/{recipe_id}")
def map_alias(alias_id: int, recipe_id: int, db: Session = Depends(get_db)):
    from .models_sales import OrderAlias, OrderItem
    alias = db.query(OrderAlias).get(alias_id)
    alias.recipe_id = recipe_id
    db.commit()
    # TODO: optionally recalc existing order_items
    return {"status": "ok"}
