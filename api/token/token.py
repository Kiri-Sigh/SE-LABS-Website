from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.model import Person
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await db.execute(db.query(Person).filter(Person.gmail == email))
    user = user.scalar_one_or_none()
    if not user or not await verify_password(password, user.user_credentials.password_hash):
        return False
    return user

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt