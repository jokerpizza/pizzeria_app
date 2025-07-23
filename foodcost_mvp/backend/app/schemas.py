from pydantic import BaseModel
from typing import List

class IngredientBase(BaseModel):
    name: str
    unit: str
    unit_price: float

class IngredientCreate(IngredientBase):
    pass

class IngredientRead(IngredientBase):
    id: int
    class Config:
        orm_mode = True

class RecipeItemBase(BaseModel):
    ingredient_id: int
    quantity: float

class RecipeItemCreate(RecipeItemBase):
    pass

class RecipeItemRead(RecipeItemBase):
    id: int
    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    name: str
    sale_price: float
    category: str

class RecipeCreate(RecipeBase):
    items: List[RecipeItemCreate]

class RecipeRead(RecipeBase):
    id: int
    items: List[RecipeItemRead]
    class Config:
        orm_mode = True