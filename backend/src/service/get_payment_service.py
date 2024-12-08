from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.payment_repository import PaymentRepository
from src.tables.payment_base import PaymentBase

async def get_payment(db: AsyncSession, 
                payment_id: int) -> PaymentBase:
    return await PaymentRepository(db).get_payment(payment_id)