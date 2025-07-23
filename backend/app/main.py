from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import products, recipes, dashboard, categories, settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FoodCost API V2", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

app.include_router(products.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(settings.router, prefix="/api")

@app.get("/api/health")
def health(): return {"status":"ok"}
