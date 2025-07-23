from typing import Sequence
from ..schemas import RecipeItemOut

def calc_food_cost(items: Sequence[RecipeItemOut]) -> float:
    return round(sum(it.quantity * it.product.price_per_unit for it in items), 2)

def calc_food_cost_pct(food_cost: float, sale_price: float) -> float:
    if sale_price == 0:
        return 0.0
    return round((food_cost / sale_price) * 100, 2)

def calc_margin(food_cost: float, sale_price: float) -> float:
    return round(sale_price - food_cost, 2)
