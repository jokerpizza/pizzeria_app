from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import products, recipes, dashboard

# Create tables (simple MVP, no Alembic yet)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FoodCost API", version="0.1.0")

import asyncio
from .sales import scheduler as sales_scheduler
from .sales import router as sales_router

# CORS - allow all for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(sales_router.router, prefix="/api")


@app.on_event("startup")
async def start_sales_scheduler():
    asyncio.create_task(sales_scheduler.loop())


@app.get("/api/health")
def health():
    return {"status": "ok"}
