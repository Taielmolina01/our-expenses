from pydantic import BaseModel
from typing import Optional

class GroupModel(BaseModel):
    name: str

    class ConfigDict:
        orm_mode = True 

class GroupUpdate(BaseModel):
    name: Optional[str] = None

    class ConfigDict:
        orm_mode = True 
