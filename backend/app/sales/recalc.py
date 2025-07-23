
from .models_sales import SessionLocal, OrderItem, OrderAlias

def recompute_costs(alias_id: int) -> int:
    db = SessionLocal()
    try:
        alias = db.query(OrderAlias).get(alias_id)
        if not alias or not alias.recipe_id:
            return 0
        items = db.query(OrderItem).filter(OrderItem.meal_name == alias.papu_name).all()
        changed = 0
        for it in items:
            cost_unit = alias.recipe.food_cost
            it.recipe_id = alias.recipe_id
            it.cost_unit = cost_unit
            it.margin_unit = it.price_unit - cost_unit
            changed += 1
        db.commit()
        return changed
    finally:
        db.close()
