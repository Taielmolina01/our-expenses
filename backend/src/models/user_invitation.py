from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserInvitationModel(BaseModel):
    invitator_email: str
    guest_email: str
    group_id: int
    send_date: date
    expire_date: date

    class ConfigDict:
        orm_mode = True 

class UserInvitationUpdate(BaseModel):
    invitator_email: Optional[str] = None
    guest_email: Optional[str] = None
    group_id: Optional[int] = None
    send_date: Optional[date] = None
    expire_date: Optional[date] = None

    class ConfigDict:
        orm_mode = True 