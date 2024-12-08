from pydantic import BaseModel
from typing import Optional

class UserInGroupModel(BaseModel):
    group_id: int
    user_email: str
    balance: float = 0.0

    class ConfigDict:
        orm_mode = True 

class UserInGroupUpdate(BaseModel):
    group_id: int
    user_email: str
    balance: Optional[float]

    class ConfigDict:
        orm_mode = True 