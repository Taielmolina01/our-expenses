from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user_in_group import UserInGroupModel, UserInGroupUpdate
from src.tables.user_in_group_base import UserInGroupBase
from src.repository.group_repository import GroupRepository
from src.repository.user_repository import UserRepository
from src.repository.user_in_group_repository import UserInGroupRepository
from src.service.get_group_service import *
from src.service.exceptions.groups_exceptions import GroupNotRegistered
from src.service.exceptions.users_exceptions import UserNotRegistered
from src.service.exceptions.users_by_groups_exceptions import UserNotRegisteredInGroup

def create_user_in_group(user_in_group_model: UserInGroupModel) -> UserInGroupBase:
    return UserInGroupBase(
        group_id=user_in_group_model.group_id,
        user_email=user_in_group_model.user_email,
        balance=0.0
    )

class UserInGroupService:

    def __init__(self, 
                 db: AsyncSession):
        self.group_repository = GroupRepository(db)
        self.user_repository = UserRepository(db)
        self.user_in_group_repository = UserInGroupRepository(db)

    async def __checks_if_user_and_group_exists(self,
                                  user_email: str,
                                  group_id: int):
        if not await self.user_repository.get_user(user_email):
            raise UserNotRegistered(user_email)
        if not await self.group_repository.get_group(group_id):
            raise GroupNotRegistered()
        
    async def is_user_in_group(self,
                               user_email: str,
                               group_id: int):
        await self.__checks_if_user_and_group_exists(user_email, group_id)
        return await self.user_in_group_repository.get_user_in_group(user_email=user_email, group_id=group_id) is not None

    async def create_user_in_group(self,
                       user_in_group: UserInGroupModel) -> UserInGroupBase:
        if not await self.user_repository.get_user(user_in_group.user_email):
            raise UserNotRegistered(user_in_group.user_email)
        if not await self.group_repository.get_group(user_in_group.group_id):
            raise GroupNotRegistered()
        return await self.user_in_group_repository.create_user_in_group(create_user_in_group(user_in_group))

    async def get_user_in_group(self,
                                user_email: str,
                                group_id: int) -> UserInGroupBase:
        await self.__checks_if_user_and_group_exists(user_email, group_id)
        return await self.user_in_group_repository.get_user_in_group(user_email=user_email, group_id=group_id)
    
    async def get_groups_by_user(self,
                            user_email: str) -> list[UserInGroupBase]:
        if not await self.user_repository.get_user(user_email):
            raise UserNotRegistered(user_email)
        return await self.user_in_group_repository.get_groups_by_user(user_email) 
    
    async def get_groups_data_by_user(self,
                            user_email: str) -> list[UserInGroupBase]:
        if not await self.user_repository.get_user(user_email):
            raise UserNotRegistered(user_email)
        return await self.user_in_group_repository.get_groups_data_by_user(user_email) 

    async def get_users_by_group(self,
                              group_id: int) -> list[UserInGroupBase]:
        if not await self.group_repository.get_group(group_id=group_id):
            raise GroupNotRegistered()
        return await self.user_in_group_repository.get_users_by_group(group_id=group_id)
    
    async def get_users_data_by_group(self,
                            group_id: int) -> list[UserInGroupBase]:
        if not await self.group_repository.get_group(group_id):
            raise GroupNotRegistered()
        return await self.user_in_group_repository.get_users_data_by_group(group_id) 

    async def update_user_in_group(self,
                       balance_update: UserInGroupUpdate) -> UserInGroupBase:
        registered_balance = await self.get_user_in_group(balance_update.user_email, balance_update.group_id)
        if balance_update.balance is not None:
            registered_balance.balance = balance_update.balance
        return await self.user_in_group_repository.update_user_in_group(registered_balance)

    async def delete_user_in_group(self,
                       user_email: str,
                       group_id: int) -> bool:
        registered_balance = await self.get_user_in_group(user_email, group_id)
        return await self.user_in_group_repository.delete_user_in_group(registered_balance)