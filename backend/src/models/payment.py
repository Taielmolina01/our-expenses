from pydantic import BaseModel, validator
from typing import Optional
import enum
from datetime import date

class Category(enum.Enum):
    FOOD = 0
    UTILITIES = 1
    CLOTHING = 2
    HEALTHCARE = 3
    PERSONAL = 4
    EDUCATION = 5
    GIFTS = 6
    ENTERTAINMENT = 7
    OTHERS = 8

class PaymentModel(BaseModel):
    group_id: int
    description: str
    payer_email: str
    payment_date: str
    category: Category
    amount: float

    class ConfigDict:
        orm_mode = True 

class PaymentUpdate(BaseModel):
    group_id: Optional[int] = None
    description: Optional[str] = None
    payer_email: Optional[str] = None
    payment_date: Optional[str] = None
    category: Optional[Category] = None
    amount: Optional[float] = None

    class ConfigDict:
        orm_mode = True 