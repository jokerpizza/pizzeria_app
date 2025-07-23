from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# Product
class ProductBase(BaseModel):
    name: str
    base_unit: str = "kg"
    price_per_unit: float

class ProductCreate(ProductBase): ...
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    base_unit: Optional[str] = None
    price_per_unit: Optional[float] = None
class ProductOut(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Category
class CategoryBase(BaseModel):
    name: str
class CategoryCreate(CategoryBase): ...
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
class CategoryOut(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ProdCat
class ProdCatBase(BaseModel):
    product_id: int
    category_id: int
class ProdCatCreate(ProdCatBase): ...
class ProdCatOut(ProdCatBase):
    id: int
    product: ProductOut | None = None
    category: CategoryOut | None = None
    model_config = ConfigDict(from_attributes=True)

# Recipe / Items
class RecipeItemBase(BaseModel):
    product_id: int
    quantity: float
class RecipeItemCreate(RecipeItemBase): ...
class RecipeItemOut(RecipeItemBase):
    id: int
    product: ProductOut
    model_config = ConfigDict(from_attributes=True)

class RecipeBase(BaseModel):
    name: str
    portion_size: float = 1.0
    sale_price: float = 0.0
class RecipeCreate(RecipeBase):
    items: List[RecipeItemCreate] = []
class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    portion_size: Optional[float] = None
    sale_price: Optional[float] = None
    items: Optional[List[RecipeItemCreate]] = None

class RecipeOut(RecipeBase):
    id: int
    items: List[RecipeItemOut] = []
    food_cost: float
    food_cost_pct: float
    margin: float
    model_config = ConfigDict(from_attributes=True)
