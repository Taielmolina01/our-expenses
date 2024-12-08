from sqlalchemy.future import select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from src.tables.debt_base import DebtBase
from src.tables.user_base import UserBase
from src.tables.group_base import GroupBase
from src.tables.payment_base import PaymentBase
from src.models.debt import DebtState

class DebtRepository:

    def __init__(self, 
                 db: AsyncSession):
        self.db = db

    async def create_debt(self, 
                    debt: DebtBase) -> DebtBase:
        self.db.add(debt)
        await self.db.commit()
        await self.db.refresh(debt)
        return debt

    async def get_debt(self, 
                 debt_id: int) -> DebtBase:
        query = select(DebtBase).where(DebtBase.debt_id == debt_id)
        result = await self.db.execute(query)
        return result.scalars().first()
    
    async def get_debts_by_user_and_group(self, 
                                    user_email: str, 
                                    group_id: int) -> list[DebtBase]:
        query = select(DebtBase).where(DebtBase.debtor_email == user_email, DebtBase.group_id == group_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_debts_by_debtor(self, 
                            user_email: str) -> list[DebtBase]:
        query = select(DebtBase).where(DebtBase.debtor_email == user_email)
        result = await self.db.execute(query)
        return result.scalars().all()    
    
    async def get_debts_by_creditor(self, 
                              user_email: str) -> list[DebtBase]:
        query = select(DebtBase).where(DebtBase.creditor_email == user_email)
        result = await self.db.execute(query)
        return result.scalars().all()  
    
    async def get_debts_by_user_data(self,
                                     user_email: str) -> list:
            
        debtor = aliased(UserBase)
        creditor = aliased(UserBase)
        group = aliased(GroupBase)
        
        query = (
            select(
                DebtBase.debt_id.label('debt_id'),
                PaymentBase.description.label('payment_description'),
                debtor.name.label('debtor_name'),
                creditor.name.label('creditor_name'),
                (DebtBase.percentage * PaymentBase.amount).label('calculated_amount'),
                DebtBase.state.label('debt_state'),
                group.name.label('group_name')
            )
            .join(PaymentBase, DebtBase.payment_id == PaymentBase.payment_id)
            .join(debtor, DebtBase.debtor_email == debtor.email)
            .join(creditor, DebtBase.creditor_email == creditor.email)
            .join(group, DebtBase.group_id == group.group_id)
            .where(
                (DebtBase.debtor_email == user_email) | (DebtBase.creditor_email == user_email)
            )  
        )

        result = await self.db.execute(query)
        debts = result.all()

        debts_data = []
        for debt_id, payment_description, debtor_name, creditor_name, calculated_amount, debt_state, group_name in debts:
            debt_state_name = DebtState(debt_state).name  
            debts_data.append({
                "debt_id": debt_id,
                "payment_description": payment_description,
                "debtor_name": debtor_name,
                "creditor_name": creditor_name,
                "calculated_amount": calculated_amount,
                "debt_state": debt_state_name,
                "group_name": group_name
            })
        
        return debts_data

    async def get_debts_by_group(self, 
                           group_id: int) -> list[DebtBase]:
        query = select(DebtBase).where(DebtBase.group_id == group_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_debts_by_group_data(self, 
                           group_id: int) -> list[DebtBase]:
        debtor = aliased(UserBase)
        creditor = aliased(UserBase)
        
        query = (
            select(
                DebtBase.debt_id.label('debt_id'),
                PaymentBase.description.label('payment_description'),
                debtor.name.label('debtor_name'),
                debtor.email.label('debtor_email'),
                creditor.name.label('creditor_name'),
                creditor.email.label('creditor_email'),
                (DebtBase.percentage * PaymentBase.amount).label('calculated_amount'),
                DebtBase.state.label('debt_state')
            )
            .join(PaymentBase, DebtBase.payment_id == PaymentBase.payment_id)
            .join(debtor, DebtBase.debtor_email == debtor.email)
            .join(creditor, DebtBase.creditor_email == creditor.email)
            .where(DebtBase.group_id == group_id)
        )

        result = await self.db.execute(query)
        debts = result.all()

        debts_data = []
        for debt_id, payment_description, debtor_name, debtor_email, creditor_name, creditor_email, calculated_amount, debt_state in debts:
            debt_state_name = DebtState(debt_state).name
            debts_data.append({
                "debt_id": debt_id,
                "payment_description": payment_description,
                "debtor_name": debtor_name,
                "debtor_email": debtor_email,
                "creditor_name": creditor_name,
                "creditor_email": creditor_email,
                "calculated_amount": calculated_amount,
                "debt_state": debt_state_name
            })
        
        return debts_data
        
    async def get_debts_by_payment_id(self, 
                                payment_id: int) -> list[DebtBase]:
        query = select(DebtBase).where(DebtBase.payment_id == payment_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_debt(self, 
                    debt: DebtBase) -> DebtBase:
        await self.db.commit()
        await self.db.refresh(debt)
        return debt
    
    async def delete_debt(self, 
                    debt: DebtBase) -> bool:
        await self.db.delete(debt)
        await self.db.commit()
        return True