
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    papu_id = Column(Integer, unique=True, nullable=False)
    finished_at = Column(DateTime, default=datetime.utcnow, index=True)
    total_price = Column(Float, default=0.0)
    localization_id = Column(Integer)

    items = relationship("OrderItem", back_populates="order", cascade="all,delete")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    meal_name = Column(String, nullable=False)
    qty = Column(Integer, default=1)
    price_unit = Column(Float, default=0.0)

    # mapping to recipe (can be null initially)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="SET NULL"), nullable=True)

    cost_unit = Column(Float, default=0.0)
    margin_unit = Column(Float, default=0.0)

    order = relationship("Order", back_populates="items")
    recipe = relationship("Recipe", uselist=False)

class OrderAlias(Base):
    __tablename__ = "order_aliases"
    id = Column(Integer, primary_key=True, index=True)
    papu_name = Column(String, unique=True, nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="SET NULL"), nullable=True)

    recipe = relationship("Recipe", uselist=False)
