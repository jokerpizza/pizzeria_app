import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.session import Base, engine, get_db
from app import models  # <-- WAŻNE: rejestruje modele w Base!
from app.api import ingredients, recipes, orders, mappings
from app.api.metrics import router as metrics_router

# Utworzenie tabel (gdy backend startuje pierwszy raz)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FoodCost",
    version="0.2.0",
    openapi_url="/api/openapi.json",
)

# ----- CORS -----
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Routers -----
app.include_router(ingredients.router, prefix="/api/ingredients", tags=["ingredients"])
app.include_router(recipes.router,      prefix="/api/recipes",      tags=["recipes"])
app.include_router(mappings.router,     prefix="/api/mappings",     tags=["mappings"])
app.include_router(orders.router,       prefix="/api/orders",       tags=["orders"])
app.include_router(metrics_router, prefix="/api/metrics", tags=["metrics"])

# ----- Health -----
@app.get("/api/health")
def health():
    return {"status": "ok"}

# ----- DEBUG (usuń później) -----
@app.get("/api/debug/count")
def debug_count(db: Session = Depends(get_db)):
    return {
        "orders": db.query(models.Order).count(),
        "items":  db.query(models.OrderItem).count(),
    }

@app.get("/api/debug/dburl")
def debug_dburl():
    url = os.getenv("DATABASE_URL", "")
    # zamaskuj hasło
    masked = url.split("@")[-1] if "@" in url else url
    return {"db": masked[:60] + ("..." if len(masked) > 60 else "")}