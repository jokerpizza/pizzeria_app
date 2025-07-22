from fastapi import FastAPI
from .routers import products, recipes, dashboard, categories

app = FastAPI()

app.include_router(products.router)
app.include_router(recipes.router)
app.include_router(dashboard.router)
app.include_router(categories.router)