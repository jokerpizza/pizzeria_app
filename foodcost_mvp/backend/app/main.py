from fastapi import FastAPI
from .db.session import engine, Base
from .api.ingredients import router as ingredients_router
from .api.recipes import router as recipes_router

# Create tables via SQLAlchemy (for development; migrations handled by Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(ingredients_router, prefix='/ingredients', tags=['ingredients'])
app.include_router(recipes_router, prefix='/recipes', tags=['recipes'])