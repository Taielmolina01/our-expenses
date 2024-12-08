from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
PASSWORD_CONTEXT_SCHEME = os.getenv("PASSWORD_CONTEXT_SCHEME")
PASSWORD_CONTEXT_DEPRECATED = os.getenv("PASSWORD_CONTEXT_DEPRECATED")
OAUTH2_SCHEME_TOKEN_URL = os.getenv("OAUTH2_SCHEME_TOKEN_URL")
PASSWORD_CONTEXT = CryptContext(schemes=[PASSWORD_CONTEXT_SCHEME], deprecated=PASSWORD_CONTEXT_DEPRECATED)
OAUTH2SCHEME = OAuth2PasswordBearer(tokenUrl=OAUTH2_SCHEME_TOKEN_URL)

def verify_password(plain_password, hashed_password):
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(plain_password):
    return PASSWORD_CONTEXT.hash(plain_password)
