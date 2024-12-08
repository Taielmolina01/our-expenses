from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.tables.user_in_group_base import UserInGroupBase
from src.tables.user_base import UserBase
from src.tables.group_base import GroupBase

class UserInGroupRepository:

    def __init__(self, 
                 db: AsyncSession):
        self.db = db

    async def create_user_in_group(self, 
                    user_in_group: UserInGroupBase) -> UserInGroupBase:
        self.db.add(user_in_group)
        await self.db.commit()
        await self.db.refresh(user_in_group)
        return user_in_group

    async def get_user_in_group(self, 
                user_email: str,
                group_id: int) -> UserInGroupBase:
        query = select(UserInGroupBase).where(UserInGroupBase.user_email == user_email, UserInGroupBase.group_id == group_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def get_users_by_group(self, 
                            group_id: int) -> list[UserInGroupBase]:
        
        query = select(UserInGroupBase).where(UserInGroupBase.group_id == group_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_users_data_by_group(self, 
                                    group_id: int) -> list[dict]:
        query = (
            select(UserInGroupBase, UserBase)
            .join(UserBase, UserBase.email == UserInGroupBase.user_email)
            .where(UserInGroupBase.group_id == group_id)
        )
        result = await self.db.execute(query)
        balances_with_user_info = result.all()

        return [
            {
                "group_id": balance.group_id,
                "balance": balance.balance,
                "user_name": user.name,
                "user_email": user.email,
            }
            for balance, user in balances_with_user_info
        ]
    
    async def get_groups_by_user(self, 
                             user_email: str) -> list[UserInGroupBase]:
        query = select(UserInGroupBase).where(UserInGroupBase.user_email == user_email)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_groups_data_by_user(self, user_email: str):
        query = (
            select(GroupBase, UserInGroupBase)
            .join(UserInGroupBase, UserInGroupBase.group_id == GroupBase.group_id)
            .where(UserInGroupBase.user_email == user_email)
        )
        result = await self.db.execute(query)
        user_groups_with_balances = result.all()

        return [
            {
                "group_id": group.group_id,
                "group_name": group.name,
                "user_email": balance.user_email,
                "balance": balance.balance,
            }
            for group, balance in user_groups_with_balances
        ]
    
    async def update_user_in_group(self, 
                    user_in_group: UserInGroupBase) -> UserInGroupBase:
        await self.db.commit()
        await self.db.refresh(user_in_group)
        return user_in_group
    
    async def delete_user_in_group(self, 
                    user_in_group: UserInGroupBase) -> bool:
        await self.db.delete(user_in_group)
        await self.db.commit()
        return True