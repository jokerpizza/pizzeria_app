
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import products, recipes, dashboard

# sales imports
from .sales.router import router as sales_router
from .sales.scheduler import scheduler as sales_scheduler

# Create tables (simple MVP, no Alembic yet)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FoodCost API", version="0.1.0")

# CORS - allow all for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(sales_router)

@app.on_event("startup")
async def start_sales_scheduler():
    import asyncio
    asyncio.create_task(sales_scheduler())

@app.get("/api/health")
def health():
    return {"status": "ok"}
