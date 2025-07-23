from pydantic import BaseModel

# ----------- PRODUCT -----------
class ProductBase(BaseModel):
    name: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

ProductOut = Product

# ----------- CATEGORY -----------
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

# ----------- RECIPE -----------
class RecipeBase(BaseModel):
    name: str
    category_id: int | None = None

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    class Config:
        orm_mode = True