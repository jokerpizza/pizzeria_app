from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    unit = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    sale_price = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    items = relationship("RecipeItem", back_populates="recipe", cascade="all, delete")

class RecipeItem(Base):
    __tablename__ = "recipe_items"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity = Column(Float, nullable=False)

    recipe = relationship("Recipe", back_populates="items")
    ingredient = relationship("Ingredient")
    __table_args__ = (UniqueConstraint('recipe_id','ingredient_id', name='uix_recipe_ing'),)

class Order(Base):
    __tablename__="orders"
    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    number = Column(String, nullable=True)
    source = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    localization = Column(String, nullable=True)
    raw_json = Column(String, nullable=True)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

class OrderItem(Base):
    __tablename__="order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    name = Column(String, nullable=False)
    size_name = Column(String, nullable=True)
    category_name = Column(String, nullable=True)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")

class NameMapping(Base):
    __tablename__="name_mappings"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    alias = Column(String, unique=True, nullable=False)

    recipe = relationship("Recipe")
