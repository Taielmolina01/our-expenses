from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.service.debt_service import *
from src.database.database import get_database
from src.controller.login_controller import get_current_active_user
from src.tables.user_base import UserBase
from src.models.user_in_group import UserInGroupModel, UserInGroupUpdate
from src.service.user_in_group_service import UserInGroupService
from src.service.exceptions.users_exceptions import UserNotRegistered
from src.service.exceptions.groups_exceptions import GroupNotRegistered
from src.service.exceptions.users_by_groups_exceptions import UserNotRegisteredInGroup

router = APIRouter()

@router.post("/groups/{group_id}/users/{user_email}")
async def create_user_in_group(group_id: int,
                                user_email: str,
                                db: AsyncSession = Depends(get_database),
                                current_user: UserBase = Depends(get_current_active_user)):
    try: 
        user_in_group = UserInGroupModel(group_id=group_id, user_email=user_email, balance=0)
        return await UserInGroupService(db).create_user_in_group(user_in_group)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except GroupNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserNotRegisteredInGroup as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get("/groups/{group_id}/users")
async def get_users_by_group(group_id: int,
                                db: AsyncSession = Depends(get_database),
                                current_user: UserBase = Depends(get_current_active_user)):
    try: 
        return await UserInGroupService(db).get_users_by_group(group_id)
    except GroupNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    
@router.get("/groups/{group_id}/users/data")
async def get_users_data_by_group(group_id: int, 
                                  db: AsyncSession = Depends(get_database),
                                  current_user: UserBase = Depends(get_current_active_user)):
    return await UserInGroupService(db).get_users_data_by_group(group_id)
    
@router.get("/users/{user_email}/groups")
async def get_groups_by_user(user_email: str,
                               db: AsyncSession = Depends(get_database),
                               current_user: UserBase = Depends(get_current_active_user)):
    try:
        return await UserInGroupService(db).get_groups_by_user(user_email)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    
@router.get("/users/{user_email}/groups/data")
async def get_groups_data_by_user(user_email: str, 
                                  db: AsyncSession = Depends(get_database),
                                  current_user: UserBase = Depends(get_current_active_user)):
    return await UserInGroupService(db).get_groups_data_by_user(user_email)

@router.get("/groups/{group_id}/users/{user_email}")
async def get_user_in_group(user_email: str,
                            group_id: int,
                            db: AsyncSession = Depends(get_database),
                            current_user: UserBase = Depends(get_current_active_user)):
    try: 
        return await UserInGroupService(db).get_user_in_group(user_email, group_id)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except GroupNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserNotRegisteredInGroup as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.put("/groups/{group_id}/users/{user_email}")
async def update_user_in_group(balance_update: UserInGroupUpdate,
                        db: AsyncSession = Depends(get_database),
                        current_user: UserBase = Depends(get_current_active_user)):
    try: 
        return await UserInGroupService(db).update_user_in_group(balance_update)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except GroupNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserNotRegisteredInGroup as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.post("/groups/{group_id}/users/{user_email}")
async def delete_user_in_group(group_id: int,
                               user_email: str,
                        db: AsyncSession = Depends(get_database),
                        current_user: UserBase = Depends(get_current_active_user)):
    try: 
        user_in_group = await UserInGroupService(db).get_user_in_group(group_id=group_id, user_email=user_email)
        return await UserInGroupService(db).delete_user_in_group(user_in_group)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except GroupNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserNotRegisteredInGroup as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
