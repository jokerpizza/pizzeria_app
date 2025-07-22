from pydantic import BaseModel, validator
from typing import Optional, List

def non_negative(v):
    if v < 0:
        raise ValueError("wartość musi być >= 0")
    return v

# Categories
class ProdCatBase(BaseModel):
    name: str
class ProdCatCreate(ProdCatBase): ...
class ProdCatOut(ProdCatBase):
    id:int
    class Config: from_attributes=True

class RecCatBase(BaseModel):
    name: str
class RecCatCreate(RecCatBase): ...
class RecCatOut(RecCatBase):
    id:int
    class Config: from_attributes=True

# Product
class ProductBase(BaseModel):
    name:str
    base_unit:str
    price_per_kg:float
    category_id: Optional[int]=None
    _p = validator("price_per_kg", allow_reuse=True)(non_negative)
class ProductCreate(ProductBase): ...
class ProductUpdate(ProductBase): ...
class ProductOut(ProductBase):
    id:int
    category_name: Optional[str]=None
    class Config: from_attributes=True

# Recipe items
class ItemIn(BaseModel):
    product_id: Optional[int]=None
    semi_id: Optional[int]=None
    amount: float
    unit: str
    _a = validator("amount", allow_reuse=True)(non_negative)

class ItemOut(BaseModel):
    id:int
    product_id: Optional[int]
    semi_id: Optional[int]
    product_name: Optional[str]
    semi_name: Optional[str]
    amount: float
    unit: str

# Recipe
class RecipeBase(BaseModel):
    name:str
    sale_price: Optional[float]=None
    is_semi: bool=False
    category_id: Optional[int]=None
    _s = validator("sale_price", allow_reuse=True)(lambda v: non_negative(v) if v is not None else v)

class RecipeCreate(RecipeBase):
    items: List[ItemIn]

class RecipeUpdate(RecipeBase):
    items: List[ItemIn]

class RecipeOut(RecipeBase):
    id:int
    items: List[ItemOut]
    cost: float
    food_cost_pct: float
    margin: float
    alert: bool
    category_name: Optional[str]=None
    class Config: from_attributes=True

# Dashboard
class DashOut(BaseModel):
    product_count:int
    avg_food_cost_pct:float
    top5_expensive:list
    alerts:list

# Settings
class SettingsOut(BaseModel):
    fc_threshold: float
class SettingsIn(BaseModel):
    fc_threshold: float
    _t = validator("fc_threshold", allow_reuse=True)(non_negative)
