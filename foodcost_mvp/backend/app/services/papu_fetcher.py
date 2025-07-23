import os
import requests
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine, Base
from app import models

# Utworzenie tabel (gdy worker startuje bez backendu)
Base.metadata.create_all(bind=engine)

API_URL = os.getenv("PAPU_URL", "https://rest.papu.io/api/orders/order-meal/list-objects/")
TOKEN = os.getenv("PAPU_TOKEN")
LOCALIZATION = os.getenv("PAPU_LOCALIZATION", "801")

FIELDS = (
    "id,name,size_name,category_name,meal_set_name,order_menu_source,"
    "order_finished_at,order_finished_type,order_number,order_menu_brand_name,"
    "is_printed,bill_position_value,bill_position_quantity"
)

# ---------- Helpers ----------

def parse_papu_dt(val: str):
    """Obsłuż różne formaty dat zwracane przez PAPU."""
    if not val:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%d-%m-%Y %H:%M", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            return datetime.strptime(val, fmt)
        except ValueError:
            continue
    print("Nieznany format daty z PAPU:", val)
    return None

def fetch_page(after: str, before: str, page: int, page_size: int = 50):
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Referer": "https://admin.papu.io/",
    }
    payload = {
        "is_printed": None,
        "meal_options": [],
        "order__finished_at_after": after,
        "order__finished_at_before": before,
        "order__finished_type": ["delivered", "finished"],
        "order__localization": int(LOCALIZATION),
        "order__menu__brand": [],
        "order__menu__source": [],
        "page": page,
        "page_size": page_size,
        "fields": FIELDS,
        "group_by_name": False,
        "summarize": True,
    }

    r = requests.post(API_URL, headers=headers, json=payload, timeout=30)

    # DEBUG 401
    if r.status_code == 401:
        print("401 Unauthorized from PAPU API")
        print("Authorization header starts with:", headers["Authorization"][:25], "...")
        print("Response text:", r.text)

    r.raise_for_status()
    return r.json()

def fetch_orders(after: str, before: str):
    """Pobierz wszystkie strony wyników między after/before."""
    page = 1
    all_results = []
    while True:
        data = fetch_page(after, before, page=page, page_size=50)
        results = data.get("results", [])
        all_results.extend(results)
        # brak klucza 'next' w tej strukturze – sprawdzamy liczbę wyników
        if len(results) < 50:
            break
        page += 1
    return {"results": all_results}

# ---------- DB save ----------

def save_to_db(data: dict, db: Session):
    inserted_orders = 0
    inserted_items = 0

    for obj in data.get("results", []):
        ext_id = str(obj["id"])
        if db.query(models.Order).filter_by(external_id=ext_id).first():
            continue

        order = models.Order(
            external_id=ext_id,
            finished_at=parse_papu_dt(obj.get("order_finished_at")),
            number=obj.get("order_number"),
            source=obj.get("order_menu_source"),
            brand=obj.get("order_menu_brand_name"),
            localization=str(obj.get("order__localization", "")),
            raw_json=str(obj),
        )
        db.add(order)
        db.flush()
        inserted_orders += 1

        item = models.OrderItem(
            order_id=order.id,
            name=obj["name"],
            size_name=obj.get("size_name"),
            category_name=obj.get("category_name"),
            quantity=float(obj.get("bill_position_quantity") or 1),
            price=float(obj.get("bill_position_value") or 0),
        )
        db.add(item)
        inserted_items += 1

    db.commit()
    print(f"Zapisano: {inserted_orders} zamówień, {inserted_items} pozycji.")

# ---------- Main sync ----------

def run_sync():
    db = SessionLocal()
    try:
        last = db.query(models.Order).order_by(models.Order.id.desc()).first()
        now = datetime.now(timezone.utc)
        after_dt = last.finished_at if (last and last.finished_at) else now - timedelta(days=1)

        after = after_dt.strftime("%Y-%m-%d %H:%M")
        before = now.strftime("%Y-%m-%d %H:%M")

        print(f"SYNC START: {after} -> {before}")
        try:
            data = fetch_orders(after, before)
        except requests.HTTPError as e:
            print("HTTPError:", e)
            return
        except Exception as e:
            print("Unhandled error while fetching orders:", e)
            return

        save_to_db(data, db)
        print("SYNC OK.")
    finally:
        db.close()

if __name__ == "__main__":
    run_sync()
