from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    base_unit = Column(String, nullable=False)  # kg, g, l, ml, szt
    price_per_kg = Column(Float, nullable=False)  # PLN per kg (or per unit if szt)

    recipe_items = relationship("RecipeItem", back_populates="product", cascade="all,delete")

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    sale_price = Column(Float, nullable=False)  # PLN

    items = relationship("RecipeItem", back_populates="recipe", cascade="all,delete")

class RecipeItem(Base):
    __tablename__ = "recipe_items"
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    amount = Column(Float, nullable=False)
    unit = Column(String, nullable=False)  # kg, g, l, ml, szt

    recipe = relationship("Recipe", back_populates="items")
    product = relationship("Product", back_populates="recipe_items")
