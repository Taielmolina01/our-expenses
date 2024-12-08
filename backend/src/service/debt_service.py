from sqlalchemy.ext.asyncio import AsyncSession
from src.service.get_payment_service import get_payment
from src.models.user import UserUpdate
from src.tables.debt_base import DebtBase
from src.models.debt import DebtModel, DebtState, DebtUpdate
from src.repository.debt_repository import DebtRepository
from src.service.exceptions.debts_exceptions import *
from src.service.user_service import UserService
from src.service.group_service import GroupService
from src.service.user_in_group_service import UserInGroupService
from src.models.user_in_group import UserInGroupUpdate

def create_debt_from_model(debt_model: DebtModel) -> DebtBase:
    return DebtBase(
        payment_id = debt_model.payment_id,
        group_id = debt_model.group_id,
        debtor_email = debt_model.debtor_email,
        creditor_email = debt_model.creditor_email,
        percentage = debt_model.percentage,
        state = debt_model.state
    )

class DebtService:

    def __init__(self,
                 db: AsyncSession):
        self.debt_repository = DebtRepository(db)
        self.user_service = UserService(db)
        self.user_in_group_service = UserInGroupService(db)
        self.group_service = GroupService(db)
        self.db = db

    async def create_debt(self,
                    debt: DebtModel) -> DebtBase:
        return await self.debt_repository.create_debt(create_debt_from_model(debt))
        
    async def get_debt(self,
                 debt_id: int) -> DebtBase:
        return await self.debt_repository.get_debt(debt_id)
    
    async def get_debts_by_user_and_group(self, 
                                    user_email: str, 
                                    group_id: int) -> list[DebtBase]:
        return await self.debt_repository.get_debts_by_user_and_group(user_email, group_id)
    
    async def get_debts_by_debtor(self, 
                            user_email: str) -> list[DebtBase]:
        return await self.debt_repository.get_debts_by_debtor(user_email)
    
    async def get_debts_by_creditor(self, 
                              user_email: str) -> list[DebtBase]:
        return await self.debt_repository.get_debts_by_creditor(user_email)
    
    async def get_debts_by_user_data(self,
                                     user_email: str) -> list[DebtBase]:
        return await self.debt_repository.get_debts_by_user_data(user_email)

    async def get_debts_by_group(self, 
                           group_id: int) -> list[DebtBase]:
        self.group_service.get_group(group_id=group_id)
        return await self.debt_repository.get_debts_by_group(group_id)
    
    async def get_debts_by_group_data(self, 
                           group_id: int) -> list[DebtBase]:
        self.group_service.get_group(group_id=group_id)
        return await self.debt_repository.get_debts_by_group_data(group_id)

    async def get_debts_by_payment_id(self, 
                                payment_id: int) -> list[DebtBase]:
        return await self.debt_repository.get_debts_by_payment_id(payment_id)
            
    async def update_debt(self,
                    debt_id: int,
                    debt_update: DebtUpdate) -> DebtBase:
        debt = await self.get_debt(debt_id)
        if not debt:
            raise DebtNotRegistered(debt_id)
        if debt_update.creditor_email:
            debt.creditor_email = debt_update.creditor_email
        if debt_update.debtor_email:
            debt.debtor_email = debt_update.debtor_email
        if debt_update.group_id:
            debt.group_id = debt_update.group_id
        if debt_update.payment_id:
            debt.payment_id = debt_update.payment_id
        if debt_update.percentage:
            debt.percentage = debt_update.percentage
            await self.__update_users_in_groups(debt, debt_update)
        if debt_update.state is not None:
            await self.__update_users_in_groups(debt, debt_update)
            debt.state = debt_update.state
        return await self.debt_repository.update_debt(debt)

    async def __update_users_in_groups(self,
                        original_debt: DebtBase,
                        debt_update: DebtUpdate):
        payment = await get_payment(self.db, original_debt.payment_id)
        amount = payment.amount

        debtor = await self.user_in_group_service.get_user_in_group(original_debt.debtor_email, original_debt.group_id)
        creditor = await self.user_in_group_service.get_user_in_group(original_debt.creditor_email, original_debt.group_id)

        balance_debtor = debtor.balance
        balance_creditor = creditor.balance

        if debt_update.state is not None and debt_update.state != original_debt.state:

            if debt_update.state == DebtState.PAID and original_debt.state == DebtState.UNPAID:

                balance_debtor -= amount * original_debt.percentage
                balance_creditor += amount * original_debt.percentage
                
            elif debt_update.state == DebtState.UNPAID and original_debt.state == DebtState.PAID:

                balance_debtor += amount * original_debt.percentage
                balance_creditor -= amount * original_debt.percentage

        if debt_update.percentage is not None and debt_update.percentage != original_debt.percentage:

            difference = debt_update.percentage - original_debt.percentage
            amount_change = amount * difference

            balance_debtor -= amount_change
            balance_creditor += amount_change

        await self.user_in_group_service.update_user_in_group(UserInGroupUpdate(group_id=payment.group_id,
                                                                    user_email=original_debt.debtor_email,
                                                                    balance=balance_debtor))
        await self.user_in_group_service.update_user_in_group(UserInGroupUpdate(group_id=payment.group_id,
                                                                    user_email=original_debt.creditor_email,
                                                                    balance=balance_creditor))

    async def delete_debt(self,
                    debt: DebtModel) -> bool:
        registered_debt = await self.get_debt(debt.debt_id)
        if not registered_debt:
            raise DebtNotRegistered(debt.debt_id)
        return await self.debt_repository.delete_debt(registered_debt)