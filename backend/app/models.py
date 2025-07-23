from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, UniqueConstraint
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    base_unit: Mapped[str] = mapped_column(String, nullable=False, default="kg")
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    recipe_items = relationship("RecipeItem", back_populates="product", cascade="all, delete")
    categories = relationship("ProdCat", back_populates="product", cascade="all, delete")

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    products = relationship("ProdCat", back_populates="category", cascade="all, delete")

class ProdCat(Base):
    __tablename__ = "prod_cat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    product = relationship("Product", back_populates="categories")
    category = relationship("Category", back_populates="products")

    __table_args__ = (UniqueConstraint("product_id", "category_id", name="uq_product_category"),)

class Recipe(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    portion_size: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    sale_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    items = relationship("RecipeItem", back_populates="recipe", cascade="all, delete-orphan")

class RecipeItem(Base):
    __tablename__ = "recipe_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    recipe = relationship("Recipe", back_populates="items")
    product = relationship("Product", back_populates="recipe_items")
