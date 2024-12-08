from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.user_repository import UserRepository
from src.models.user import UserModel, UserUpdate
from src.tables.user_base import UserBase
from src.service.exceptions.users_exceptions import *
from src.utils.login_utils import get_password_hash

def create_user_from_model(user_model: UserModel) -> UserBase:
    return UserBase(
        email=user_model.email,
        name=user_model.name,
        password=user_model.password 
    )

class UserService:

    def __init__(self,
                db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def create_user(self,
                    user: UserModel) -> UserBase:
        registered_user = await self.user_repository.get_user(user.email)
        if registered_user:
           raise UserAlreadyRegistered(user.email)
        if not user.name:
           raise UserWithoutName()
        return await self.user_repository.create_user(create_user_from_model(user))
       
    async def get_user(self, 
                 user_email: str) -> UserBase:
        user = await self.user_repository.get_user(user_email)
        if not user:
            raise UserNotRegistered(user_email)
        return user
       
    async def get_users(self) -> list[UserBase]:
       return await self.user_repository.get_users() 

    async def update_user(self, 
                    user_email: str, 
                    user_update: UserUpdate) -> UserBase:
        user = await self.get_user(user_email)
        if user_update.name is not None:            
            if user_update.name == "":
                raise UserWithoutName()
            user.name = user_update.name
        if user_update.password is not None:
            if user_update.password == "":
                raise PasswordCanNotBeEmpty()
            user.password = get_password_hash(user_update.password)
        return await self.user_repository.update_user(user)
        
       
    async def delete_user(self, 
                    user: UserBase) -> bool:
       user = await self.get_user(user.email)
       return await self.user_repository.delete_user(user)