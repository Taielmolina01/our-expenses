from pydantic import BaseModel
from typing import Optional
import enum

class DebtState(enum.Enum):
    UNPAID = 0
    PAID = 1

class DebtRole(str, enum.Enum):
    debtor = "debtor"
    creditor = "creditor"

class DebtModel(BaseModel):
    payment_id: int
    group_id: int
    debtor_email: str
    creditor_email: str
    percentage: float
    state: Optional[DebtState] = DebtState.UNPAID

    class ConfigDict:
        orm_mode = True 

class DebtUpdate(BaseModel):
    payment_id: Optional[int] = None
    group_id: Optional[int] = None
    debtor_email: Optional[str] = None
    creditor_email: Optional[str] = None
    percentage: Optional[float] = None
    state: Optional[DebtState] = None

    class ConfigDict:
        orm_mode = True 