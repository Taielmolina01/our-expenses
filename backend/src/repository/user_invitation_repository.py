from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.tables.user_invitation_base import UserInvitationBase
from src.tables.user_base import UserBase
from src.tables.group_base import GroupBase

class UserInvitationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_invitation(self, 
                          invitation: UserInvitationBase) -> UserInvitationBase:
        self.db.add(invitation)
        await self.db.commit()
        await self.db.refresh(invitation)
        return invitation
    
    async def get_invitation(self,
                             invitation_id: int) -> UserInvitationBase:
        query = select(UserInvitationBase).where(UserInvitationBase.invitation_id == invitation_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def delete_invitation(self, 
                                invitation: UserInvitationBase):
        await self.db.delete(invitation)
        await self.db.commit()
        return True

    async def get_invitations_by_guest(self, 
                                 guest_email: str) -> list[UserInvitationBase]:
        query = select(UserInvitationBase).where(UserInvitationBase.guest_email == guest_email)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_invitations_by_guest_data(self, 
                                 guest_email: str) -> list[UserInvitationBase]:
        query = (
            select(
                UserInvitationBase.invitation_id,
                UserInvitationBase.invitator_email,
                UserInvitationBase.group_id,
                UserInvitationBase.send_date,
                UserInvitationBase.expire_date,
                UserBase.name.label("invitator_name"),
                GroupBase.name.label("group_name"),
            )
            .join(UserBase, UserBase.email == UserInvitationBase.invitator_email)
            .join(GroupBase, GroupBase.group_id == UserInvitationBase.group_id)
            .where(UserInvitationBase.guest_email == guest_email)
        )
        
        result = await self.db.execute(query)
        return [
            {
                "invitation_id": row.invitation_id,
                "invitator_email": row.invitator_email,
                "invitator_name": row.invitator_name,
                "group_id": row.group_id,
                "group_name": row.group_name,
                "send_date": row.send_date,
                "expire_date": row.expire_date,
            }
            for row in result.fetchall()
        ]
