
import os, logging, datetime, requests
from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import SessionLocal
from .models_sales import Order, OrderItem, OrderAlias
from ..crud import compute_recipe_totals

PAPU_API_URL = "https://rest.papu.io/api/orders/order-meal/list-objects/"
TOKEN = os.getenv("PAPU_API_TOKEN")
LOCATION_ID = int(os.getenv("PAPU_LOCATION_ID", "0"))

logger = logging.getLogger("papu_ingestor")

def _request_orders(start: datetime.datetime, end: datetime.datetime) -> List[Dict]:
    headers = {
        "authorization": f"token {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json",
    }
    page = 1
    results = []
    while True:
        body = {
            "order__finished_at_after": start.strftime("%Y-%m-%d %H:%M"),
            "order__finished_at_before": end.strftime("%Y-%m-%d %H:%M"),
            "order__localization": LOCATION_ID,
            "page": page,
            "page_size": 50
        }
        resp = requests.post(PAPU_API_URL, json=body, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        batch = data.get("results", [])
        if not batch:
            break
        results.extend(batch)
        if data.get("next") is None:
            break
        page += 1
    return results

def fetch_and_store():
    """Fetch last 5 minutes of orders and persist."""
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(minutes=5)

    if not TOKEN or LOCATION_ID == 0:
        logger.warning("PAPU_API_TOKEN or PAPU_LOCATION_ID not configured; skip fetch.")
        return

    rows = _request_orders(start, end)

    db: Session = SessionLocal()
    for row in rows:
        papu_id = row.get("order_meal_id") or row.get("id")
        if papu_id is None:
            continue
        # de‑dupe
        if db.query(Order).filter_by(papu_id=papu_id).first():
            continue
        order = Order(
            papu_id=papu_id,
            finished_at=datetime.datetime.fromisoformat(row.get("order__finished_at")),
            total_price=row.get("order_meal_total_price", 0.0),
            localization_id=row.get("order__localization")
        )
        db.add(order)
        for item in row.get("items", []) if isinstance(row.get("items"), list) else [row]:
            meal_name = item.get("meal_name") or item.get("name") or "Unknown"
            qty = item.get("qty") or item.get("quantity") or 1
            price_unit = item.get("price") or item.get("order_meal_price") or 0.0

            alias = db.query(OrderAlias).filter_by(papu_name=meal_name).first()
            if alias is None:
                # create alias with unknown recipe
                alias = OrderAlias(papu_name=meal_name)
                db.add(alias)
                db.flush()

            if alias.recipe_id is not None:
                # mapped recipe
                recipe = alias.recipe
                cost, _, _ = compute_recipe_totals(recipe)
                cost_unit = cost
            else:
                # placeholder 30% cost
                cost_unit = round(price_unit * 0.30, 2)

            margin_unit = round(price_unit - cost_unit, 2)

            order_item = OrderItem(
                meal_name=meal_name,
                qty=qty,
                price_unit=price_unit,
                recipe_id=alias.recipe_id,
                cost_unit=cost_unit,
                margin_unit=margin_unit
            )
            order.items.append(order_item)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
    db.close()
