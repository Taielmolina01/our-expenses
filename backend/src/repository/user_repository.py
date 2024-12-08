from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.tables.user_base import UserBase

class UserRepository:

    def __init__(self, 
                 db: AsyncSession):
        self.db = db

    async def create_user(self, 
                    user: UserBase) -> UserBase:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_users(self) -> list[UserBase]:
        query = select(UserBase)
        result = await self.db.execute(query)
        return result.scalars().all()
        
    async def get_user(self, 
                 email: str) -> UserBase:
        query = select(UserBase).where(UserBase.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def update_user(self, 
                    user: UserBase) -> UserBase:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, 
                    user: UserBase) -> bool:
        await self.db.delete(user)
        await self.db.commit()
        return True