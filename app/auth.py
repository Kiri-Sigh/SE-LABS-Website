import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Union

from .model import *
from .schemas.auth_user import  AuthUser, AuthUserWithPassword, TokenData, User
from .dependencies import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_initial_admin(db):
    admin_email = os.getenv("INITIAL_ADMIN_EMAIL")
    admin_password = os.getenv("INITIAL_ADMIN_PASSWORD")
    
    if not admin_email or not admin_password:
        raise ValueError("INITIAL_ADMIN_EMAIL and INITIAL_ADMIN_PASSWORD must be set in the .env file")

    # Check if any users exist
    existing_user = db.query(Researcher).first()
    if existing_user:
        return None  # Users already exist, don't create initial admin

    # Create the admin user
    hashed_password = get_password_hash(admin_password)
    new_admin = Researcher(
        gmail=admin_email,
        hashed_password=hashed_password,
        is_admin=True,
        is_active=True
        # Add any other required fields for your Researcher model
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def get_user(db, gmail: EmailStr) -> AuthUserWithPassword:
    researcher = db.query(Researcher).filter(Researcher.gmail == gmail).first()
    if not researcher:
        # Try to create the initial admin user
        initial_admin = create_initial_admin(db)
        if initial_admin and initial_admin.gmail == gmail:
            return initial_admin
        raise HTTPException(status_code=404, detail="User not found")
    return researcher

def authenticate_user(db, gmail: EmailStr, password: str) -> Union[AuthUser, bool]:
    user = get_user(db, gmail)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(get_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(get_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return User(
        username=user.gmail,
        email=user.gmail,
        disabled=not user.is_active,
        is_admin=user.is_admin  # Add this line
    )

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user