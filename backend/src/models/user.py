from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    email: str
    name: str
    password: str

    class ConfigDict:
        orm_mode = True 

class UserResponseModel(BaseModel):
    email: str
    name: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None

    class ConfigDict:
        orm_mode = True 

class UserPassChangeUpdate(BaseModel):
    currentPassword: Optional[str] = None
    newPassword: Optional[str] = None
    user: UserUpdate