from sqlalchemy import Column, Integer, ForeignKey, String, Date
from src.database.database import Base
from datetime import datetime, timedelta, timezone

class UserInvitationBase(Base):
    __tablename__ = "invitations"

    invitation_id = Column(Integer, primary_key=True, autoincrement=True)
    invitator_email = Column(String, ForeignKey("users.email"))
    guest_email = Column(String, ForeignKey("users.email"))
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    send_date = Column(Date, default=lambda: datetime.now(timezone.utc).date())
    expire_date = Column(Date, default=lambda: (datetime.now(timezone.utc) + timedelta(days=7)).date())