from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.group_repository import GroupRepository
from src.tables.group_base import GroupBase

async def get_group_pub(db: AsyncSession, 
                  group_id: int) -> GroupBase:
    return await GroupRepository(db).get_group(group_id)