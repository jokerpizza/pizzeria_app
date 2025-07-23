import os,requests
from datetime import datetime,timezone,timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal,engine,Base
from app import models

Base.metadata.create_all(bind=engine)
API_URL=os.getenv("PAPU_URL","https://rest.papu.io/api/orders/order-meal/list-objects/")
TOKEN=os.getenv("PAPU_TOKEN")
LOCALIZATION=os.getenv("PAPU_LOCALIZATION","801")
FIELDS="id,name,size_name,category_name,order_menu_source,order_finished_at,order_finished_type,order_number,bill_position_value,bill_position_quantity"

def get_mapping(db,name,size):
    return db.query(models.NameMapping).filter_by(papu_name=name,papu_size=size).first()

def food_cost_for_recipe(db,recipe_id):
    recipe=db.query(models.Recipe).get(recipe_id)
    if not recipe:return 0
    cost=0
    for item in recipe.items:
        cost+=item.quantity*item.ingredient.price
    return cost

def fetch(after,before):
    headers={"Authorization":f"token {TOKEN}","Content-Type":"application/json"}
    payload={"order__finished_at_after":after,"order__finished_at_before":before,
        "order__finished_type":["delivered","finished"],"order__localization":int(LOCALIZATION),
        "page":1,"page_size":50,"fields":FIELDS,"group_by_name":False,"summarize":True}
    r=requests.post(API_URL,headers=headers,json=payload,timeout=30)
    r.raise_for_status()
    return r.json()

def parse_dt(val:str):
    for fmt in ("%Y-%m-%d %H:%M","%d-%m-%Y %H:%M"): 
        try:return datetime.strptime(val,fmt)
        except:continue
    return None

def run_sync():
    db=SessionLocal()
    last=db.query(models.Order).order_by(models.Order.id.desc()).first()
    now=datetime.now(timezone.utc)
    after_dt=last.finished_at if last and last.finished_at else now-timedelta(days=1)
    after=after_dt.strftime("%Y-%m-%d %H:%M")
    before=now.strftime("%Y-%m-%d %H:%M")
    data=fetch(after,before)
    for obj in data.get("results",[]):
        ext_id=str(obj["id"])
        if db.query(models.Order).filter_by(external_id=ext_id).first():continue
        mapping=get_mapping(db,obj["name"],obj.get("size_name"))
        recipe_id=mapping.recipe_id if mapping else None
        cost=food_cost_for_recipe(db,recipe_id) if recipe_id else None
        margin=None
        price_total=float(obj.get("bill_position_value") or 0)
        if cost is not None: margin=price_total-cost
        order=models.Order(external_id=ext_id,finished_at=parse_dt(obj.get("order_finished_at")),
            number=obj.get("order_number"),source=obj.get("order_menu_source"),
            recipe_id=recipe_id,food_cost=cost,margin=margin,raw_json=str(obj))
        db.add(order)
        db.flush()
        item=models.OrderItem(order_id=order.id,name=obj["name"],size_name=obj.get("size_name"),
            category_name=obj.get("category_name"),quantity=float(obj.get("bill_position_quantity") or 1),
            price=price_total)
        db.add(item)
    db.commit()
    db.close()

if __name__=="__main__":run_sync()
