from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.payment_repository import PaymentRepository
from src.models.payment import PaymentModel, PaymentUpdate
from src.service.exceptions.groups_exceptions import UserNotAuthorized
from src.tables.payment_base import PaymentBase
from src.service.exceptions.payments_exceptions import *
from src.service.user_in_group_service import UserInGroupService
from src.service.debt_service import DebtService
from src.service.user_service import UserService
from src.service.user_in_group_service import UserInGroupService
from src.models.debt import DebtModel, DebtUpdate
from src.models.user_in_group import UserInGroupUpdate
from datetime import datetime

def create_payment_from_model(payment_model: PaymentModel) -> PaymentBase:
    return PaymentBase(
        group_id = payment_model.group_id,
        payer_email = payment_model.payer_email,
        payment_date = payment_model.payment_date,
        category = payment_model.category,
        amount = payment_model.amount,
        description = payment_model.description
    )

class PaymentService:

    def __init__(self,
                 db: AsyncSession):
        self.payment_repository = PaymentRepository(db)
        self.debt_service = DebtService(db)
        self.user_service = UserService(db)
        self.user_in_group_service = UserInGroupService(db)

    async def create_payment(self,
                       payment: PaymentModel,
                       percentages: dict[str, float]) -> PaymentBase:
        users = await self.user_in_group_service.get_users_by_group(payment.group_id)

        if len(percentages) > len(users):
            raise PaymentWithMoreDistributionsThanGroupUsers()
        if len(users) > len(percentages):
            raise PaymentWithLessDistributionsThanGroupUsers()
        for (u, _) in percentages.items():
            if not u in [user.user_email for user in users]:
                raise UserNotAuthorized()
        try:
            payment.payment_date = datetime.strptime(payment.payment_date, "%Y-%m-%d")
        except ValueError:
            raise PaymentDateIsInvalid()
        
        payment_response = await self.payment_repository.create_payment(create_payment_from_model(payment))

        if len(users) == 1:
            return payment_response

        for u in users:
            user = await self.user_service.get_user(u.user_email)
            userBalanceGroup = await self.user_in_group_service.get_user_in_group(u.user_email, payment.group_id)
            if user.email == payment.payer_email:
                response = await self.user_in_group_service.update_user_in_group(UserInGroupUpdate(user_email=user.email,
                                                                                   group_id=payment.group_id,
                                                                                   balance=userBalanceGroup.balance - payment.amount + percentages[user.email] * payment.amount))
                print(f"My update payer response: {response}")
            else:
                if percentages[user.email] != 0.0:
                    debt_response = await self.debt_service.create_debt(DebtModel(payment_id=payment_response.payment_id, 
                                                            group_id=payment.group_id, 
                                                            debtor_email=user.email, 
                                                            creditor_email=payment.payer_email, 
                                                            percentage=percentages[user.email]))
                    print(f"My debt response: {debt_response}")
                    update_debtor_response = await self.user_in_group_service.update_user_in_group(UserInGroupUpdate(user_email=user.email,
                                                                                    group_id=payment.group_id,
                                                                                    balance=userBalanceGroup.balance + percentages[user.email] * payment.amount))
                    print(f"My update debtor response: {update_debtor_response}")

        
        return payment_response

        
    async def get_payment(self,
                    payment_id: int) -> PaymentBase:
        return await self.payment_repository.get_payment(payment_id)
    
    async def get_payments_by_group(self,
                              group_id: int) -> list[PaymentBase]:
        return await self.payment_repository.get_payments_by_group(group_id)
    
    async def get_payments_by_group_data(self,
                              group_id: int) -> list[PaymentBase]:
        return await self.payment_repository.get_payments_by_group_data(group_id)

    async def get_payments_by_user(self,
                              user_email: str) -> list[PaymentBase]:
        return await self.payment_repository.get_payments_by_user(user_email)
    
    async def get_payments_by_user_data(self,
                              user_email: str) -> list[PaymentBase]:
        return await self.payment_repository.get_payments_by_user_data(user_email)
    
    async def get_payments_by_user_and_group(self,
                              user_id: int,
                              group_id: int) -> list[PaymentBase]:
        return await self.payment_repository.get_payments_by_user_and_group(user_id, group_id)
    
    async def __get_original_percentages(self, payment: PaymentBase) -> dict[str, float]:
        debts = await self.debt_service.get_debts_by_payment_id(payment.payment_id)
        answer = {}
        for d in debts:
            answer[d.debtor_email] = d.percentage
        return answer

    async def update_payment(self,
                    payment_id: int,
                    payment_update: PaymentUpdate,
                    new_percentages: dict[str, float]) -> PaymentBase:

        registered_payment = await self.get_payment(payment_id)
        if not registered_payment:
            raise PaymentNotRegistered()
        
        original_percentages = await self.__get_original_percentages(registered_payment)

        if payment_update.group_id:
            registered_payment.group_id = payment_update.group_id
        if payment_update.description:
            registered_payment.description = payment_update.description
        if payment_update.payer_email:
            registered_payment.payer_email = payment_update.payer_email
        if payment_update.payment_date:
            registered_payment.payment_date = payment_update.payment_date
        if payment_update.category:
            registered_payment.category = payment_update.category
        if payment_update.amount:
            registered_payment.amount = payment_update.amount

        users = await self.user_by_group.get_users_by_group(payment_update.group_id)
        
        if len(new_percentages) > len(users):
            raise PaymentWithMoreDistributionsThanGroupUsers()
        if len(users) > len(new_percentages):
            raise PaymentWithLessDistributionsThanGroupUsers()
        
        for u in users:
            user = await self.user_service.get_user(u.user_email)
            registered_balance_in_group = await self.user_in_group_service.get_user_in_group(user_email=user.email, 
                                                                                                       group_id=registered_payment.group_id).balance
            
            if user.email == payment_update.payer_email:
                original_share = original_percentages.get(user.email, 0) * registered_payment.amount
                new_share = new_percentages.get(user.email, 0) * payment_update.amount
                updated_balance_in_group = registered_balance_in_group + registered_payment.amount - original_share
                updated_balance_in_group -= payment_update.amount - new_share
                await self.user_in_group_service.update_user_in_group(UserInGroupUpdate(group_id=registered_payment.group_id,
                                                                                   user_email=user.email,
                                                                                   balance=updated_balance_in_group))
            else:
                original_debt = original_percentages.get(user.email, 0) * registered_payment.amount
                new_debt = new_percentages.get(user.email, 0) * payment_update.amount
                updated_balance_in_group = registered_balance_in_group + original_debt - new_debt

                await self.debt_service.update_debt(DebtUpdate(
                    payment_id=payment_update.payment_id,
                    group_id=payment_update.group_id,
                    debtor_email=user.user_email,
                    creditor_email=payment_update.payer_email,
                    percentage=new_percentages[user.email]
                ))

                await self.user_in_group_service.update_user_in_group(UserInGroupUpdate(group_id=registered_payment.group_id,
                                                                                   user_email=user.email,
                                                                                   balance=updated_balance_in_group))
    
        return await self.payment_repository.update_payment(registered_payment)


    async def delete_payment(self,
                       payment: PaymentModel) -> bool:
        registered_payment = await self.get_payment(payment.payment_id)
        if not registered_payment:
            raise PaymentNotRegistered()
        debts = await self.debt_service.get_debts_by_payment_id(payment.payment_id)
        for d in debts:
            user = await self.user_service.get_user(d.debtor_email)
            registered_balance_in_group = await self.user_in_group_service.get_user_in_group(user_email=user.email, 
                                                                                                       group_id=registered_payment.group_id).balance
            await self.debt_service.delete_debt(d)
            await self.user_in_group_service.update_user_in_group(UserInGroupUpdate(group_id=registered_payment.group_id,
                                                                               user_email=d.debtor_email,
                                                                               balance=registered_balance_in_group - d.percentage * registered_payment.amount))
        payer = await self.user_service.get_user(registered_payment.payer_email)
        registered_balance_in_group = await self.user_in_group_service.get_user_in_group(user_email=payer.email, 
                                                                                                   group_id=registered_payment.group_id).balance

        await self.user_in_group_service.update_user_in_group(UserInGroupUpdate(group_id=registered_payment.group_id,
                                                                               user_email=d.debtor_email,
                                                                               balance=registered_balance_in_group + registered_payment.amount))
        return await self.payment_repository.delete_payment(registered_payment)