from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from app.db.session import Base, engine, get_db
from app import models
from app.api import ingredients, recipes, orders, mappings

Base.metadata.create_all(bind=engine)

cors_raw=os.getenv("CORS_ORIGINS","*")
origins=["*"] if cors_raw=="*" else [o.strip() for o in cors_raw.split(",") if o.strip()]

app=FastAPI(title="FoodCost",version="0.3.0",openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingredients.router,prefix="/api/ingredients",tags=["ingredients"])
app.include_router(recipes.router,prefix="/api/recipes",tags=["recipes"])
app.include_router(mappings.router,prefix="/api/mappings",tags=["mappings"])
app.include_router(orders.router,prefix="/api/orders",tags=["orders"])

@app.get("/api/health")
def health():
    return {"status":"ok"}

@app.get("/api/debug/count")
def debug_count(db:Session=Depends(get_db)):
    return {
        "orders": db.query(models.Order).count(),
        "items": db.query(models.OrderItem).count(),
        "mappings": db.query(models.NameMapping).count()
    }
