
from .db_session import SessionLocal
from .models_sales import OrderItem, OrderAlias

def recompute_costs(alias_id: int) -> int:
    db = SessionLocal()
    try:
        alias = db.query(OrderAlias).get(alias_id)
        if not alias or not alias.recipe:
            return 0
        cost = alias.recipe.food_cost
        items = db.query(OrderItem).filter_by(alias_id=alias_id).all()
        for it in items:
            it.cost_unit = cost
            it.margin_pln = (it.price_unit - cost) * it.qty
            it.margin_pct = (it.margin_pln / (it.price_unit * it.qty)) * 100 if it.price_unit else 0
        db.commit()
        return len(items)
    finally:
        db.close()
