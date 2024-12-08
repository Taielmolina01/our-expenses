from sqlalchemy import Column, Integer, Float, ForeignKey, String
from src.database.database import Base

class UserInGroupBase(Base):
    __tablename__ = "balance_by_group"

    group_id = Column(Integer, ForeignKey("groups.group_id"), primary_key=True)
    user_email = Column(String, ForeignKey("users.email"), primary_key=True)
    balance = Column(Float)

    def __repr__(self):
        return (
            f"UserInGroupBase("
            f"group_id={self.group_id}, "
            f"user_email={self.user_email}, "
            f"balance={self.balance}"
            ")"
        )