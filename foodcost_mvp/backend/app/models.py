from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    unit = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    sale_price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    items = relationship('RecipeItem', back_populates='recipe', cascade='all, delete-orphan')

class RecipeItem(Base):
    __tablename__ = 'recipe_items'
    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    recipe = relationship('Recipe', back_populates='items')