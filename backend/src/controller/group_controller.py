from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.service.group_service import *
from src.database.database import get_database
from src.tables.user_base import UserBase
from src.models.group import GroupModel, GroupUpdate
from src.controller.login_controller import get_current_active_user
from src.models.user import UserModel
from src.service.user_in_group_service import UserInGroupService
from src.models.user_in_group import UserInGroupModel

router = APIRouter()

@router.post("/groups")
async def create_group(group: GroupModel,
                       db: AsyncSession = Depends(get_database),
                       current_user: UserBase = Depends(get_current_active_user)):
    try:
        group = await GroupService(db).create_group(group)
        await UserInGroupService(db).create_user_in_group(UserInGroupModel(
            group_id=group.group_id,
            user_email=current_user.email
        ))
        return group
    except GroupWithoutName as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")
    
@router.get("/groups/{group_id}")
async def get_group(group_id: int,
                    db: AsyncSession = Depends(get_database),
                    current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await GroupService(db).get_group(group_id)
    except GroupNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.put("/groups/{group_id}")
async def update_group(group_id: int,
                       group_update: GroupUpdate,
                       db: AsyncSession = Depends(get_database),
                       current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await GroupService(db).update_group(group_id, group_update)
    except GroupNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except GroupWithoutName as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.delete("/groups/{group_id}")
async def delete_group(group_id: int,
                       db: AsyncSession = Depends(get_database),
                       current_user: UserModel = Depends(get_current_active_user)):
    try:
        return await GroupService(db).delete_group(group_id, current_user)
    except GroupNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserNotAuthorized as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")