from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    base_unit: str = "kg"
    price_per_unit: float

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    base_unit: Optional[str]
    price_per_unit: Optional[float]

class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True

class RecipeItemBase(BaseModel):
    product_id: int
    quantity: float

class RecipeItemCreate(RecipeItemBase):
    pass

class RecipeItemOut(RecipeItemBase):
    id: int
    product: ProductOut
    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    name: str
    portion_size: float = 1.0
    sale_price: float = 0.0

class RecipeCreate(RecipeBase):
    items: List[RecipeItemCreate] = []

class RecipeUpdate(BaseModel):
    name: Optional[str]
    portion_size: Optional[float]
    sale_price: Optional[float]
    items: Optional[List[RecipeItemCreate]]

class RecipeOut(RecipeBase):
    id: int
    items: List[RecipeItemOut] = []
    food_cost: float
    food_cost_pct: float
    margin: float
    class Config:
        orm_mode = True
