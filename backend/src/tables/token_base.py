from sqlalchemy import Column, ForeignKey, Boolean, DateTime, String
from src.database.database import Base
import datetime

class TokenBase(Base):
    __tablename__ = "tokens"
    user_email = Column(String, ForeignKey('users.email'))
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)