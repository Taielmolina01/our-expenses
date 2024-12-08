from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.tables.payment_base import PaymentBase
from src.tables.group_base import GroupBase
from src.tables.user_base import UserBase

class PaymentRepository:

    def __init__(self, 
                 db: AsyncSession):
        self.db = db

    async def create_payment(self, 
                       payment: PaymentBase) -> PaymentBase:
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_payment(self, 
                    payment_id: int) -> PaymentBase:
        query = select(PaymentBase).where(PaymentBase.payment_id == payment_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def get_payments_by_group(self, 
                              group_id: int) -> list[PaymentBase]:
        query = select(PaymentBase, UserBase.name.label("payer_name"),
            GroupBase.name.label("group_name"),).where(PaymentBase.group_id == group_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_payments_by_group_data(self, 
                              group_id: int) -> list[PaymentBase]:
        query = (
            select(PaymentBase, UserBase.name)
            .join(UserBase, PaymentBase.payer_email == UserBase.email)
            .where(PaymentBase.group_id == group_id)
        )
        result = await self.db.execute(query)

        payments = [
            {
                "payment_id": payment.payment_id,
                "description": payment.description,
                "payer_email": payment.payer_email,
                "payer_name": payer_name,
                "amount": payment.amount,
                "payment_date": payment.payment_date,
                "category": payment.category.name,
                "group_id": payment.group_id,
            }
            for payment, payer_name in result.all()
        ]
        return payments
    
    async def get_payments_by_user(self, 
                             user_email: str) -> list[PaymentBase]:
        query = select(PaymentBase).where(PaymentBase.payer_email == user_email)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_payments_by_user_data(self, 
                                        user_email: str) -> list[PaymentBase]:
        query = (
            select(PaymentBase,
            UserBase.name.label("payer_name"),
            GroupBase.name.label("group_name"))
            .join(UserBase, PaymentBase.payer_email == UserBase.email)
            .join(GroupBase, PaymentBase.group_id == GroupBase.group_id)
            .where(PaymentBase.payer_email == user_email)
        )
        result = await self.db.execute(query)

        payments = [
            {
                "payment_id": payment.payment_id,
                "description": payment.description,
                "payer_email": payment.payer_email,
                "payer_name": payer_name,
                "amount": payment.amount,
                "payment_date": payment.payment_date,
                "category": payment.category.name,
                "group_id": payment.group_id,
                "group_name": group_name,
            }
            for payment, payer_name, group_name in result.all()
        ]
        return payments

       
    async def get_payments_by_user_and_group(self, 
                                       user_email: str, 
                                       group_id: int) -> list[PaymentBase]:
        query = select(PaymentBase).where(PaymentBase.payer_email == user_email, PaymentBase.group_id == group_id)
        result = await self.db.execute(query)
        return result.scalars().all()
       
    async def update_payment(self, 
                       payment: PaymentBase) -> PaymentBase:
        await self.db.commit()
        await self.db.refresh(payment)
        return payment
    
    async def delete_payment(self, 
                       payment: PaymentBase) -> bool:
        await self.db.delete(payment)
        await self.db.commit()
        return True