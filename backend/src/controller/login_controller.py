from fastapi import APIRouter, Depends, HTTPException, status
from src.database.database import get_database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Header
from sqlalchemy.future import select

from src.service.exceptions import users_exceptions
from src.service.exceptions.users_exceptions import UserNotRegistered, WrongPassword
from src.models.token import UserLoginModel
from src.service.user_service import UserService
from src.utils.login_utils import verify_password, OAUTH2SCHEME, JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES
from src.tables.token_base import TokenBase

router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=120)
    to_encode.update({"exp": expire})
    return  jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_email: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": user_email}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

async def authenticate_user(user: UserLoginModel,
                      db: AsyncSession):
    try:
        registered_user = await UserService(db).get_user(user.email)
        if registered_user and verify_password(user.password, registered_user.password):
            return registered_user
        else:
            raise WrongPassword()
    except UserNotRegistered as e:
        raise UserNotRegistered(user.email)
    
async def get_current_active_user(token: Annotated[str, Depends(OAUTH2SCHEME)],
                           db: AsyncSession = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pueden validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    try:
        user = await UserService(db).get_user(user_email=email)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=UserNotRegistered.message) 

    return user

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), 
                                db: AsyncSession = Depends(get_database)):
    try:
        user = await authenticate_user(UserLoginModel(email=form_data.username, password=form_data.password), db)
    except WrongPassword as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)
    except UserNotRegistered as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except WrongPassword as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    refresh = create_refresh_token(user.email)

    token_db = TokenBase(user_email=user.email,
                                    access_token=access,
                                    refresh_token=refresh, 
                                    status=True)
    db.add(token_db)
    await db.commit()
    await db.refresh(token_db)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "name": user.name,
        }
    }

@router.post('/logout')
async def logout(
    db: AsyncSession = Depends(get_database), 
    authorization: str = Header(None)  # This extracts the token from the 'Authorization' header
):
    # Extract token from the Authorization header
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Token missing or malformed")
    
    token = authorization.split(" ")[1]  # Extract the token part from "Bearer <token>"

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])  # Decode the token
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")
    
    user_email = payload['sub']  # Get user email from the payload

    # Retrieve all token records and check for expired ones
    token_record = await db.execute(select(TokenBase))
    token_records = token_record.scalars().all()  # This returns a list of TokenBase objects

    info = []

    for record in token_records:
        if (datetime.now() - record.created_date).days > 1:
            info.append(record.user_email)
    
    if info:
        # Delete expired tokens
        result = await db.execute(
            select(TokenBase).where(TokenBase.user_email.in_(info))
        )
        tokens_to_delete = result.scalars().all()
        for token in tokens_to_delete:
            await db.delete(token)
        await db.commit()

    # Query the database for the existing token based on user email and token
    query = select(TokenBase).where(TokenBase.user_email == user_email, TokenBase.access_token == token)
    result = await db.execute(query)
    existing_token = result.scalar()  # Use scalar() instead of scalars().first()

    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        await db.commit()
        await db.refresh(existing_token)

    return {"message": "Logout Successfully"}
