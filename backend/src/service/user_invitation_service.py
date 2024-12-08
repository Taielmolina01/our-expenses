from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.user_invitation_repository import UserInvitationRepository
from src.tables.user_invitation_base import UserInvitationBase
from src.models.user_invitation import UserInvitationModel
from src.service.user_service import UserService
from src.models.user_in_group import UserInGroupModel
from src.service.exceptions.users_exceptions import UserNotRegistered
from src.service.user_in_group_service import UserInGroupService
from src.service.exceptions.users_by_groups_exceptions import *
from src.service.exceptions.invitation_exceptions import *

def create_invitation_from_model(user_invitation: UserInvitationModel) -> UserInvitationBase:
    return UserInvitationBase(
        invitator_email = user_invitation.invitator_email,
        guest_email = user_invitation.guest_email,
        group_id = user_invitation.group_id,
        send_date = user_invitation.send_date,
        expire_date = user_invitation.expire_date
    )

class UserInvitationService:

    def __init__(self,
                 db: AsyncSession):
        self.invitation_repository = UserInvitationRepository(db)
        self.user_service = UserService(db)
        self.user_in_group_service = UserInGroupService(db)

    async def create_invitation(self,
                          invitation: UserInvitationModel) -> UserInvitationBase:
        registered_invitator, registered_guest = await self.user_service.get_user(invitation.invitator_email), await self.user_service.get_user(invitation.guest_email)
        if not registered_invitator:
            raise UserNotRegistered(invitation.invitator_email)
        if not await self.user_in_group_service.is_user_in_group(registered_invitator.email, invitation.group_id):
            raise UserNotRegisteredInGroup(invitation)
        if not registered_guest:
            raise UserNotRegistered(invitation.guest_email)
        if await self.user_in_group_service.is_user_in_group(registered_guest.email, invitation.group_id):
            raise UserAlreadyRegisteredInGroup(registered_guest.email)
        if await self.already_invited(invitation):
            raise UserAlreadyInvitedToGroup(registered_guest.email)
        return await self.invitation_repository.create_invitation(create_invitation_from_model(invitation))
    
    async def already_invited(self, 
                              invitation: UserInvitationModel) -> bool:
        invitations_guest = await self.get_invitations_by_guest(invitation.guest_email)
        for i in invitations_guest:
            if i.group_id == invitation.group_id:
                return True
        return False

    async def get_invitation(self, 
                             invitation_id: int) -> UserInvitationBase:
        invitation = await self.invitation_repository.get_invitation(invitation_id)
        if not invitation:
            raise InvitationNotRegistered
        return invitation

    async def get_invitations_by_guest(self,
                                user_email: str) -> list[UserInvitationBase]:
        registered_user = await self.user_service.get_user(user_email)
        if not registered_user:
            raise UserNotRegistered(user_email)
        return await self.invitation_repository.get_invitations_by_guest(user_email)
    

    async def get_invitations_by_guest_data(self,
                                user_email: str) -> list[UserInvitationBase]:
        registered_user = await self.user_service.get_user(user_email)
        if not registered_user:
            raise UserNotRegistered(user_email)
        return await self.invitation_repository.get_invitations_by_guest_data(user_email)

    async def accept_invitation(self,
                                invitation_id: int):
        invitation = await self.get_invitation(invitation_id)
        userByGroup = UserInGroupModel(group_id=invitation.group_id,
                                       user_email=invitation.guest_email)
        await self.user_in_group_service.create_user_in_group(userByGroup)
        await self.invitation_repository.delete_invitation(invitation)

    
    async def reject_invitation(self, 
                                invitation_id: int):
        invitation = await self.get_invitation(invitation_id)
        await self.invitation_repository.delete_invitation(invitation)