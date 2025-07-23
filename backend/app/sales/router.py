
"""Router sales with status/count and dynamic Recipe import."""
from datetime import datetime, timedelta
from importlib import import_module
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .models_sales import OrderItem, OrderAlias
from .recalc import recompute_costs

# --- dynamic import of Recipe + compute_recipe_totals -------------------
def _find_recipe_and_calc():
    candidates = [
        ("backend.app.models", "compute_recipe_totals", "backend.app.crud"),
        ("app.models", "compute_recipe_totals", "app.crud"),
        ("backend/app/models.py", None, None),  # fallback
    ]
    recipe_cls = None
    compute_fn = None
    for mod_name_model, fn_name, crud_mod_name in candidates:
        try:
            mod_models = import_module(mod_name_model)
            if hasattr(mod_models, "Recipe"):
                recipe_cls = getattr(mod_models, "Recipe")
            if fn_name:
                compute_fn = getattr(import_module(crud_mod_name), fn_name)
            if recipe_cls:
                break
        except ModuleNotFoundError:
            continue
    if not recipe_cls:
        raise ImportError("Recipe model not found")
    return recipe_cls, compute_fn

Recipe, compute_recipe_totals = _find_recipe_and_calc()
# ------------------------------------------------------------------------

router = APIRouter(prefix="/sales", tags=["sales"])

@router.get("/live")
def sales_live(minutes: int = 5, db: Session = Depends(get_db)):
    """Return raw order items from last `minutes`."""
    since = datetime.utcnow() - timedelta(minutes=minutes)
    items = (
        db.query(OrderItem)
        .filter(OrderItem.order.has(finished_at__gte=since))
        .order_by(OrderItem.id.desc())
        .all()
    )
    def row(i):
        return {
            "id": i.id,
            "finished_at": i.order.finished_at if i.order else None,
            "name": i.alias.papu_name,
            "qty": i.qty,
            "turnover": round(i.price_unit * i.qty, 2),
            "cost": round(i.cost_unit * i.qty, 2),
            "margin": round(i.margin_pln, 2),
            "margin_pct": round(i.margin_pct, 2),
        }
    totals_turnover = sum(i.price_unit * i.qty for i in items)
    totals_margin = sum(i.margin_pln for i in items)
    totals_cost = totals_turnover - totals_margin
    return {
        "status": "ok",
        "count": len(items),
        "totals": {
            "turnover": round(totals_turnover, 2),
            "cost": round(totals_cost, 2),
            "margin": round(totals_margin, 2),
        },
        "items": [row(i) for i in items],
    }

@router.get("/aliases/unmapped")
def unmapped_aliases(db: Session = Depends(get_db)):
    rows = db.query(OrderAlias).filter(OrderAlias.recipe_id == None).all()
    return [{"id": r.id, "papu_name": r.papu_name} for r in rows]

@router.post("/aliases/{alias_id}/map/{recipe_id}")
def map_alias(alias_id: int, recipe_id: int, db: Session = Depends(get_db)):
    alias = db.query(OrderAlias).get(alias_id)
    if not alias:
        raise HTTPException(status_code=404, detail="Alias not found")
    alias.recipe_id = recipe_id
    db.commit()
    updated = recompute_costs(alias_id)
    return {"status": "ok", "items_recomputed": updated}
