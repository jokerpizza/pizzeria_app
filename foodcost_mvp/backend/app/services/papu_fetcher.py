import requests, os, datetime
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine, Base
from app import models

# <<< DODAJ TO TUŻ PO IMPORTACH >>>
Base.metadata.create_all(bind=engine)
# <<< KONIEC DODATKU >>>

API_URL=os.getenv("PAPU_URL","https://rest.papu.io/api/orders/order-meal/list-objects/")
TOKEN=os.getenv("PAPU_TOKEN")
LOCALIZATION=os.getenv("PAPU_LOCALIZATION","801")

FIELDS="id,name,size_name,category_name,meal_set_name,order_menu_source,order_finished_at,order_finished_type,order_number,order_menu_brand_name,is_printed,bill_position_value,bill_position_quantity"

def fetch_orders(after:str, before:str, page:int=1, page_size:int=50):
    headers={
        "Authorization": f"token {TOKEN}",
        "Accept":"application/json",
        "Content-Type":"application/json",
        "Referer":"https://admin.papu.io/"
    }
    payload={
        "is_printed": None,
        "meal_options": [],
        "order__finished_at_after": after,
        "order__finished_at_before": before,
        "order__finished_type": ["delivered","finished"],
        "order__localization": int(LOCALIZATION),
        "order__menu__brand": [],
        "order__menu__source": [],
        "page": page,
        "page_size": page_size,
        "fields": FIELDS,
        "group_by_name": False,
        "summarize": True
    }
    r=requests.post(API_URL, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

def save_to_db(data:dict, db:Session):
    for obj in data.get("results",[]):
        ext_id=str(obj["id"])
        if db.query(models.Order).filter_by(external_id=ext_id).first():
            continue
        order=models.Order(
            external_id=ext_id,
            finished_at=datetime.datetime.fromisoformat(obj["order_finished_at"]) if obj.get("order_finished_at") else None,
            number=obj.get("order_number"),
            source=obj.get("order_menu_source"),
            brand=obj.get("order_menu_brand_name"),
            localization=str(obj.get("order__localization","")),
            raw_json=str(obj)
        )
        db.add(order)
        db.flush()
        item=models.OrderItem(
            order_id=order.id,
            name=obj["name"],
            size_name=obj.get("size_name"),
            category_name=obj.get("category_name"),
            quantity=float(obj.get("bill_position_quantity") or 1),
            price=float(obj.get("bill_position_value") or 0)
        )
        db.add(item)
    db.commit()

def run_sync():
    db=SessionLocal()
    try:
        last=db.query(models.Order).order_by(models.Order.id.desc()).first()
        if last and last.finished_at:
            after=last.finished_at.strftime("%Y-%m-%d %H:%M")
        else:
            after=(datetime.datetime.utcnow()-datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        before=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        data=fetch_orders(after,before)
        save_to_db(data, db)
    finally:
        db.close()

if __name__=="__main__":
    run_sync()
