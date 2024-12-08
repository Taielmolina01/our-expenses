from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from src.database.database import Base
import datetime

class UserBase(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    password = Column(String, nullable=False)

class TokenBase(Base):
    __tablename__ = "token"
    user_email = Column(String, ForeignKey("users.email"))
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)