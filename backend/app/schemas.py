from pydantic import BaseModel, Field
from typing import List

# ---------- Product ----------

class ProductBase(BaseModel):
    name: str = Field(..., examples=["Mąka"])
    base_unit: str = Field(..., examples=["kg"])
    price_per_kg: float = Field(..., gt=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    class Config:
        from_attributes = True

# ---------- Recipe ----------

class RecipeItemIn(BaseModel):
    product_id: int
    amount: float
    unit: str

class RecipeBase(BaseModel):
    name: str
    sale_price: float

class RecipeCreate(RecipeBase):
    items: List[RecipeItemIn]

class RecipeUpdate(RecipeBase):
    items: List[RecipeItemIn]

class RecipeItemOut(RecipeItemIn):
    id: int
    product_name: str

class RecipeOut(RecipeBase):
    id: int
    items: List[RecipeItemOut]
    cost: float
    food_cost_pct: float
    margin: float
    class Config:
        from_attributes = True
