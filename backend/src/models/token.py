from pydantic import BaseModel
import datetime

class TokenData(BaseModel):
    access_token: str
    refresh_token: str

class TokenCreate(BaseModel):
    user_email: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime

class UserLoginModel(BaseModel):
    email: str
    password: str