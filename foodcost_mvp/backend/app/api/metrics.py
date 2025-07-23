from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.db.session import get_db
from app.models.models import Order, RecipeItem

router = APIRouter()

@router.get("/today-profit")
def get_today_profit(db: Session = Depends(get_db)):
    today = date.today()
    orders = db.query(Order).filter(Order.date_created >= today).all()
    total_revenue = 0.0
    total_cost = 0.0
    for order in orders:
        for item in order.items:
            total_revenue += item.sale_price * item.quantity
            recipe_items = db.query(RecipeItem).filter(RecipeItem.recipe_id == item.recipe_id).all()
            cost = sum(ri.quantity * ri.ingredient.price for ri in recipe_items)
            total_cost += cost * item.quantity
    return {
        "date": today.isoformat(),
        "revenue": total_revenue,
        "cost": total_cost,
        "profit": total_revenue - total_cost
    }
