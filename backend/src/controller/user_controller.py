from fastapi import APIRouter, Depends, HTTPException, status
from src.database.database import get_database
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import UserModel, UserUpdate, UserPassChangeUpdate
from src.models.token import *
from src.utils.login_utils import verify_password
from src.service.user_service import UserService
from src.service.exceptions.users_exceptions import *
from src.utils.login_utils import get_password_hash

router = APIRouter()

@router.post("/users")
async def create_user(user: UserModel, 
                      db: AsyncSession = Depends(get_database)):
    try:
        hashed_password = get_password_hash(user.password)
        new_user = UserModel(email=user.email,
                            name=user.name,
                            password=hashed_password)
        return await UserService(db).create_user(new_user)
    except UserAlreadyRegistered as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except UserWithoutName as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_database)):
    return await UserService(db).get_users() 

@router.get("/users/{user_email}")
async def get_user(user_email: str,
                   db: AsyncSession = Depends(get_database)):
    try:
        return await UserService(db).get_user(user_email)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.put("/users/{user_email}")
async def update_user(user_email: str,
                      user_update: UserUpdate,
                      db: AsyncSession = Depends(get_database)):
    try:
        return await UserService(db).update_user(user_email, user_update)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserWithoutName as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except PasswordCanNotBeEmpty as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
@router.put("/users/{user_email}/updatepass")
async def update_pass(user_email: str,
                      user_pass_update: UserPassChangeUpdate,
                      db: AsyncSession = Depends(get_database)):
    try:
        registered_user = await UserService(db).get_user(user_email)
        if registered_user and verify_password(user_pass_update.currentPassword, registered_user.password):
            user_updated = UserUpdate(name=user_pass_update.user.name, password=user_pass_update.newPassword)
            return await UserService(db).update_user(user_email, user_updated)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except UserWithoutName as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/users/{user_email}")
async def delete_user(user_email: str, 
                      db: AsyncSession = Depends(get_database)):
    try:
        return await UserService(db).delete_user(user_email)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")