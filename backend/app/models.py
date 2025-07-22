from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class ProductCategory(Base):
    __tablename__ = "product_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    products = relationship("Product", back_populates="category")

class RecipeCategory(Base):
    __tablename__ = "recipe_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    recipes = relationship("Recipe", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    base_unit = Column(String, nullable=False)  # kg,g,l,ml,szt
    price_per_kg = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=True)

    category = relationship("ProductCategory", back_populates="products")
    recipe_items = relationship("RecipeItem", back_populates="product", cascade="all,delete")

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    sale_price = Column(Float, nullable=True)
    is_semi = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey("recipe_categories.id"), nullable=True)

    category = relationship("RecipeCategory", back_populates="recipes")
    items = relationship("RecipeItem", back_populates="recipe", cascade="all,delete")

class RecipeItem(Base):
    __tablename__ = "recipe_items"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    semi_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    amount = Column(Float, nullable=False)
    unit = Column(String, nullable=False)

    recipe = relationship("Recipe", foreign_keys=[recipe_id], back_populates="items")
    product = relationship("Product", back_populates="recipe_items")
    semi = relationship("Recipe", foreign_keys=[semi_id])
