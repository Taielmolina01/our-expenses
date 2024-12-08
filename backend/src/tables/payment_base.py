from sqlalchemy import Column, Integer, Float, Date, Enum, ForeignKey, String
from src.database.database import Base
from src.models.payment import Category

class PaymentBase(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    description = Column(String)
    payer_email = Column(String, ForeignKey("users.email"))
    payment_date = Column(Date)
    category = Column(Enum(Category))
    amount = Column(Float)