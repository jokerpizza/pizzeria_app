
"""REST ingestor fetching orders every time it's called."""
import os, logging, datetime, requests
from typing import List, Dict
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .models_sales import Order, OrderItem, OrderAlias
from importlib import import_module

PAPU_API_URL = "https://rest.papu.io/api/orders/order-meal/list-objects/"
TOKEN = os.getenv("PAPU_API_TOKEN")
LOCATION_ID = int(os.getenv("PAPU_LOCATION_ID", "0"))

# compute_recipe_totals import
try:
    compute_recipe_totals = getattr(import_module("backend.app.crud"), "compute_recipe_totals")
except ModuleNotFoundError:
    from ..crud import compute_recipe_totals   # fallback

logger = logging.getLogger("papu_ingestor")

def _request_orders(start: datetime.datetime, end: datetime.datetime) -> List[Dict]:
    headers = {
        "authorization": f"token {TOKEN}",
        "accept": "application/json",
        "content-type": "application/json",
    }
    page = 1
    results: List[Dict] = []
    while True:
        body = {
            "order__finished_at_after": start.strftime("%Y-%m-%d %H:%M"),
            "order__finished_at_before": end.strftime("%Y-%m-%d %H:%M"),
            "order__localization": LOCATION_ID,
            "page": page,
            "page_size": 50,
        }
        resp = requests.post(PAPU_API_URL, json=body, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        page_results = data.get("results", [])
        results.extend(page_results)
        if len(page_results) < 50:
            break
        page += 1
    return results

def _store_rows(rows: List[Dict]):
    db: Session = SessionLocal()
    added = 0
    try:
        for row in rows:
            papu_item_id = row["id"]
            if db.query(OrderItem).filter_by(papu_item_id=papu_item_id).first():
                continue
            order_papu_id = row["order"]
            order = db.query(Order).filter_by(papu_order_id=order_papu_id).first()
            if not order:
                finished_at = datetime.datetime.fromisoformat(row["order_finished_at"]).replace(tzinfo=None)
                order = Order(papu_order_id=order_papu_id, finished_at=finished_at)
                db.add(order)
                db.flush()

            name = row.get("meal_name") or row.get("name") or "Unknown"
            alias = db.query(OrderAlias).filter_by(papu_name=name).first()
            if not alias:
                alias = OrderAlias(papu_name=name)
                db.add(alias)
                db.flush()

            qty = int(row.get("quantity", 1))
            price_unit = float(row.get("price", 0))

            if alias.recipe:
                cost_unit = compute_recipe_totals(alias.recipe)[0]
            else:
                cost_unit = price_unit * 0.30

            margin_pln = (price_unit - cost_unit) * qty
            margin_pct = (margin_pln / (price_unit * qty)) * 100 if price_unit else 0

            item = OrderItem(
                papu_item_id=papu_item_id,
                order_id=order.id,
                alias_id=alias.id,
                qty=qty,
                price_unit=price_unit,
                cost_unit=cost_unit,
                margin_pln=margin_pln,
                margin_pct=margin_pct,
            )
            db.add(item)
            added += 1
        db.commit()
    finally:
        db.close()
    return added

def fetch_and_store(hours: int = 24):
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(minutes=5)
    rows = _request_orders(start, end)
    added = _store_rows(rows)
    logger.info("Fetched %s rows", added)
    return added
