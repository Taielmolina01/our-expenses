from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.tables.group_base import GroupBase

class GroupRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_group(self, 
                     group: GroupBase) -> GroupBase:
        self.db.add(group)
        await self.db.commit()
        await self.db.refresh(group)
        return group

    async def get_group(self, 
                  group_id: int) -> GroupBase:
        query = select(GroupBase).where(GroupBase.group_id == group_id)
        result = await self.db.execute(query)
        return result.scalars().first()
        
    async def update_group(self, 
                     group: GroupBase) -> GroupBase:
        await self.db.commit()
        await self.db.refresh(group)
        return group
    
    async def delete_group(self, 
                     group: GroupBase) -> bool:
        await self.db.delete(group)
        await self.db.commit()
        return True