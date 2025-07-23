from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    base_unit = Column(String, default="kg", nullable=False)
    price_per_unit = Column(Float, nullable=False, default=0.0)

    recipe_items = relationship("RecipeItem", back_populates="product")

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    portion_size = Column(Float, nullable=False, default=1.0)  # grams or units
    sale_price = Column(Float, nullable=False, default=0.0)

    items = relationship("RecipeItem", back_populates="recipe", cascade="all, delete-orphan")

class RecipeItem(Base):
    __tablename__ = "recipe_items"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False, default=0.0)

    recipe = relationship("Recipe", back_populates="items")
    product = relationship("Product", back_populates="recipe_items")
