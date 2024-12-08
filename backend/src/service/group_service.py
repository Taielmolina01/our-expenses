from sqlalchemy.ext.asyncio import AsyncSession
from src.models.group import GroupModel, GroupUpdate
from src.models.user import UserModel
from src.service.user_in_group_service import UserInGroupService
from src.tables.group_base import GroupBase
from src.tables.user_in_group_base import UserInGroupBase
from src.repository.user_in_group_repository import UserInGroupRepository
from src.repository.group_repository import GroupRepository
from src.service.exceptions.groups_exceptions import *
from src.repository.payment_repository import PaymentRepository

def create_group_from_model(group_model: GroupModel) -> GroupBase:
    return GroupBase(
        name=group_model.name
    )

class GroupService:

    def __init__(self,
                 db: AsyncSession):
        self.group_repository = GroupRepository(db)
        self.db = db

    async def create_group(self,
                     group: GroupModel) -> GroupBase:
        if not group.name:
            raise GroupWithoutName()
        return await self.group_repository.create_group(create_group_from_model(group))

    async def get_group(self,
                group_id: int) -> GroupBase:
        group = await self.group_repository.get_group(group_id)
        if not group:
            raise GroupNotRegistered()
        return group
    
    async def update_group(self, 
                    group_id: int, 
                    group_update: GroupUpdate) -> GroupBase:
        group = await self.get_group(group_id)
        if group_update.name is not None:
            if group_update.name == "":
                raise GroupWithoutName()
            group.name = group_update.name
        return await self.group_repository.update_group(group)
    
    async def delete_group(self, group_id: int, user: UserModel) -> bool:

        group = await self.get_group(group_id)

        if not await UserInGroupService(self.db).is_user_in_group(user.email, group_id):
            raise UserNotAuthorized()

        payments = await PaymentRepository(self.db).get_payments_by_group(group_id)

        for p in payments:
            await PaymentRepository(self.db).delete_payment(p)
        
        users = await UserInGroupRepository(self.db).get_users_by_group(group_id)

        for u in users:
            await UserInGroupRepository(self.db).delete_user_in_group(u)
                                                                    

        return await self.group_repository.delete_group(group)
