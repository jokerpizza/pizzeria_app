from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import products, recipes, categories, prodcat
from .config import settings as app_settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FoodCost API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(prodcat.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok"}
