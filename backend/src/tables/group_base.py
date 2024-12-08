from sqlalchemy import Column, Integer, String
from src.database.database import Base

class GroupBase(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __repr__(self):
        return (
            f"Group("
            f"group_id={self.group_id}, "
            f"name={self.name}, "
            ")"
        )