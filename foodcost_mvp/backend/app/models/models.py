from sqlalchemy import Column,Integer,String,Float,DateTime,ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Ingredient(Base):
    __tablename__="ingredients"
    id=Column(Integer,primary_key=True)
    name=Column(String,unique=True,index=True)
    unit=Column(String)
    price=Column(Float)
    updated_at=Column(DateTime,default=datetime.utcnow)

class Recipe(Base):
    __tablename__="recipes"
    id=Column(Integer,primary_key=True)
    name=Column(String,unique=True,index=True)
    sale_price=Column(Float)
    category=Column(String)
    items=relationship("RecipeItem",back_populates="recipe",cascade="all,delete")

class RecipeItem(Base):
    __tablename__="recipe_items"
    id=Column(Integer,primary_key=True)
    recipe_id=Column(Integer,ForeignKey("recipes.id"))
    ingredient_id=Column(Integer,ForeignKey("ingredients.id"))
    quantity=Column(Float)
    recipe=relationship("Recipe",back_populates="items")
    ingredient=relationship("Ingredient")

class Order(Base):
    __tablename__="orders"
    id=Column(Integer,primary_key=True)
    external_id=Column(String,unique=True,index=True)
    finished_at=Column(DateTime)
    number=Column(String)
    source=Column(String)
    brand=Column(String)
    localization=Column(String)
    raw_json=Column(String)
    recipe_id=Column(Integer,ForeignKey("recipes.id"))
    food_cost=Column(Float)
    margin=Column(Float)
    items=relationship("OrderItem",back_populates="order",cascade="all,delete")
    recipe=relationship("Recipe")

class OrderItem(Base):
    __tablename__="order_items"
    id=Column(Integer,primary_key=True)
    order_id=Column(Integer,ForeignKey("orders.id"))
    name=Column(String)
    size_name=Column(String)
    category_name=Column(String)
    quantity=Column(Float)
    price=Column(Float)
    order=relationship("Order",back_populates="items")

class NameMapping(Base):
    __tablename__="mappings"
    id=Column(Integer,primary_key=True)
    papu_name=Column(String,index=True)
    papu_size=Column(String,index=True)
    recipe_id=Column(Integer,ForeignKey("recipes.id"))
    updated_at=Column(DateTime,default=datetime.utcnow)
    recipe=relationship("Recipe")
