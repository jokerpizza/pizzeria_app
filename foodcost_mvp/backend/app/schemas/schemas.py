from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class IngredientBase(BaseModel):
    name: str
    unit: str
    price: float

class IngredientCreate(IngredientBase):
    pass

class IngredientRead(IngredientBase):
    id: int
    updated_at: datetime
    class Config:
        from_attributes = True

class RecipeItemBase(BaseModel):
    ingredient_id: int
    quantity: float

class RecipeItemRead(RecipeItemBase):
    id: int
    class Config:
        from_attributes = True

class RecipeBase(BaseModel):
    name: str
    sale_price: float
    category: Optional[str] = None

class RecipeCreate(RecipeBase):
    items: List[RecipeItemBase]

class RecipeRead(RecipeBase):
    id: int
    items: List[RecipeItemRead]
    class Config:
        from_attributes = True

class MappingBase(BaseModel):
    alias: str
    recipe_id: int

class MappingRead(MappingBase):
    id: int
    class Config:
        from_attributes = True

class OrderItemRead(BaseModel):
    id: int
    name: str
    size_name: Optional[str]
    category_name: Optional[str]
    quantity: float
    price: float
    class Config:
        from_attributes = True

class OrderRead(BaseModel):
    id: int
    external_id: str
    finished_at: Optional[datetime]
    number: Optional[str]
    source: Optional[str]
    brand: Optional[str]
    localization: Optional[str]
    items: List[OrderItemRead]
    class Config:
        from_attributes = True
