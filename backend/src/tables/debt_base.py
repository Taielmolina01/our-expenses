from sqlalchemy import Column, Integer, Float, ForeignKey, String, Enum
from src.database.database import Base
from src.models.debt import DebtState

class DebtBase(Base):
    __tablename__ = "debts"

    debt_id = Column(Integer, primary_key=True, autoincrement=True)
    payment_id = Column(Integer, ForeignKey("payments.payment_id"))
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    debtor_email = Column(String, ForeignKey("users.email"))
    creditor_email = Column(String, ForeignKey("users.email"))
    percentage = Column(Float)
    state = Column(Enum(DebtState))