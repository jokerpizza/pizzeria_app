from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime

class MappingBase(BaseModel):
    papu_name:str
    papu_size:Optional[str]|None=None
    recipe_id:int
class MappingRead(MappingBase):
    id:int
    updated_at:datetime
    class Config:model_config={'from_attributes':True}
