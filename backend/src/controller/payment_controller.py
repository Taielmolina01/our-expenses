from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.payment import PaymentModel, PaymentUpdate
from src.database.database import get_database
from src.service.exceptions.groups_exceptions import UserNotAuthorized
from src.service.exceptions.payments_exceptions import *
from src.service.payment_service import PaymentService
from src.controller.login_controller import get_current_active_user
from src.models.user import UserModel
from src.models.payment import Category

router = APIRouter()

@router.post("/payments")
async def create_payment(payment: PaymentModel,
                         percentages: dict[str, float],
                       db: AsyncSession = Depends(get_database),
                       current_user: UserModel = Depends(get_current_active_user)):
        try:
                return await PaymentService(db).create_payment(payment, percentages)
        except PaymentWithoutDescription as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
        except PaymentWithMoreDistributionsThanGroupUsers as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        except PaymentWithLessDistributionsThanGroupUsers as e:
                raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=e.message)
        except UserNotAuthorized as e:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
        except PaymentDateIsInvalid as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
        except PaymentAmountIsInvalid as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
@router.get("/payments/options")
async def get_payment_options(current_user: UserModel = Depends(get_current_active_user)):
        return [c.name for c in Category]
        
@router.get("/payments/{payment_id}")
async def get_payment(payment_id: int,
                    db: AsyncSession = Depends(get_database),
                    current_user: UserModel = Depends(get_current_active_user)):
        try:
                return await PaymentService(db).get_payment(payment_id)
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/groups/{group_id}/payments")
async def get_payments_by_group(group_id: int,
                              db: AsyncSession = Depends(get_database),
                              current_user: UserModel = Depends(get_current_active_user)):
        try:
                return await PaymentService(db).get_payments_by_group(group_id)
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
@router.get("/groups/{group_id}/payments/data")
async def get_payments_by_group_data(group_id: int,
                              db: AsyncSession = Depends(get_database),
                              current_user: UserModel = Depends(get_current_active_user)):
        try:
                return await PaymentService(db).get_payments_by_group_data(group_id)
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/users/{user_email}/payments")
async def get_payments_by_user(user_email: str,
                              db: AsyncSession = Depends(get_database),
                              current_user: UserModel = Depends(get_current_active_user)):
        try:
                return await PaymentService(db).get_payments_by_user(user_email)
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
@router.get("/users/{user_email}/payments/data")
async def get_payments_by_user_data(user_email: str,
                              db: AsyncSession = Depends(get_database),
                              current_user: UserModel = Depends(get_current_active_user)):
        try:
                return await PaymentService(db).get_payments_by_user_data(user_email)
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/groups/{group_id}/users/{user_email}/payments")
async def get_payments_by_user_and_group(user_email: str,
                              group_id: int,
                              db: AsyncSession = Depends(get_database),
                              current_user: UserModel = Depends(get_current_active_user)):
        try:
                return await PaymentService(db).get_payments_by_user_and_group(user_email, group_id)
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.put("/payments/{payment_id}")
async def update_payment(payment_id: int,
                       payment_update: PaymentUpdate,
                       percentages: list[int],
                       db: AsyncSession = Depends(get_database),
                       current_user: UserModel = Depends(get_current_active_user)):
        try:
                return await PaymentService(db).update_payment(payment_id, payment_update, percentages)
        except PaymentWithoutDescription as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
@router.delete("/payments")
async def delete_payment(payment: PaymentModel,
                       db: AsyncSession = Depends(get_database),
                       current_user: UserModel = Depends(get_current_active_user)):
        try:
                return await PaymentService(db).delete_payment(payment)
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")