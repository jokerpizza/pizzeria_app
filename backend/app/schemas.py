from pydantic import BaseModel

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

# ... RecipeBase, RecipeCreate, Recipe itd ...
class RecipeBase(BaseModel):
    # ...inne pola...
    category_id: int | None = None  # <-- nowe pole!