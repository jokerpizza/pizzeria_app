from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .db.session import engine, Base, get_db
from .api import ingredients, recipes, orders, mappings
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FoodCost", version="0.1.0", openapi_url="/api/openapi.json")

origins = os.getenv("CORS_ORIGINS","*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingredients.router, prefix="/api/ingredients", tags=["ingredients"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["recipes"])
app.include_router(mappings.router, prefix="/api/mappings", tags=["mappings"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])

@app.get("/api/health")
def health():
    return {"status":"ok"}
