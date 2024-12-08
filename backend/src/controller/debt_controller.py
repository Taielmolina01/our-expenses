from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.service.debt_service import *
from src.database.database import get_database
from src.models.debt import DebtModel, DebtUpdate, DebtRole
from src.models.user import UserModel
from src.controller.login_controller import get_current_active_user
from src.service.exceptions.debts_exceptions import *
from src.service.exceptions.users_exceptions import *
from src.service.exceptions.groups_exceptions import *

router = APIRouter()

@router.post("/debts")
async def create_debt(debt: DebtModel,
                      db: AsyncSession = Depends(get_database),
                      current_user: UserModel = Depends(get_current_active_user)) :
    try:
        return await DebtService(db).create_debt(debt)
    except DebtAlreadyRegistered as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except DebtIsInvalid as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    
@router.get("/debts/{debt_id}")
async def get_debt(debt_id: int,
                      db: AsyncSession = Depends(get_database),
                      current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await DebtService(db).get_debt(debt_id)
    except DebtNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    

@router.get("/debts/users/{user_email}")
async def get_debts_by_user(user_email: str,
                            role: DebtRole,
                            db: AsyncSession = Depends(get_database),
                            current_user: UserModel = Depends(get_current_active_user)):
    try:
        if role.name == DebtRole.debtor:
            return await DebtService(db).get_debts_by_debtor(user_email)
        elif role.name == DebtRole.creditor:
            return await DebtService(db).get_debts_by_creditor(user_email)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El rol indiicado no existe") 
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    
@router.get("/debts/users/{user_email}/data")
async def get_debts_by_user_data(user_email: str,
                            db: AsyncSession = Depends(get_database),
                            current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await DebtService(db).get_debts_by_user_data(user_email)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    
@router.get("/debts/groups/{group_id}")
async def get_debts_by_group(group_id: int,
                            db: AsyncSession = Depends(get_database),
                            current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await DebtService(db).get_debts_by_group(group_id)
    except GroupNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    
@router.get("/debts/groups/{group_id}/data")
async def get_debts_by_group_data(group_id: int,
                            db: AsyncSession = Depends(get_database),
                            current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await DebtService(db).get_debts_by_group_data(group_id)
    except GroupNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    
@router.put("/debts/{debt_id}")
async def update_debt(debt_id: int,
                      debt_update: DebtUpdate,
                      db: AsyncSession = Depends(get_database),
                      current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await DebtService(db).update_debt(debt_id, debt_update)
    except DebtNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except DebtIsInvalid as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


@router.delete("/debts")
async def delete_debt(debt: DebtModel,
                      db: AsyncSession = Depends(get_database),
                      current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await DebtService(db).delete_debt(debt)
    except DebtNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")