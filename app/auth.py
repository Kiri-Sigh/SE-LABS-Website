import os
from dotenv import load_dotenv
from fastapi import  Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import joinedload, Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union

from .model import *
from .schemas.auth_user import  AuthUser, TokenData, Token
from .dependencies import get_db

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, gmail: str) -> Researcher:
    researcher = db.query(Researcher).options(joinedload(Researcher.user_credentials)).filter(Researcher.gmail == gmail).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="User not found")
    return researcher

def create_user(db: Session, user_data: dict, password: str):
    new_user = Researcher(**user_data)
    db.add(new_user)
    db.flush()

    hashed_password = get_password_hash(password)
    new_credentials = UserCredentials(
        user_id=new_user.user_id,
        password_hash=hashed_password
    )
    db.add(new_credentials)
    
    new_user.user_credentials = new_credentials
    
    db.commit()
    db.refresh(new_user)
    db.refresh(new_credentials)

    return new_user

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
        full_name="Admin User",
        image_high=b"not important",
        image_low=b"not important",
        gmail=admin_email,
        highest_role="admin",
        admin=True,
        active=True
        # Add any other required fields for your Researcher model
    )
    
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    new_credentials = UserCredentials(
        user_id=new_admin.user_id,
        password_hash=hashed_password
    )

    db.add(new_credentials)
    db.commit()
    db.refresh(new_credentials)

    new_admin.user_credentials = new_credentials
    db.commit()
    db.refresh(new_admin)

    return new_admin

def authenticate_user(db: Session, gmail: str, password: str) -> Union[Researcher, bool]:
    # if don't have any users, create the initial admin user and check if the user is the initial admin
    if not db.query(Researcher).first():
        initial_admin = create_initial_admin(db)
        if not initial_admin:
            return False
        if initial_admin.gmail == gmail and verify_password(password, initial_admin.user_credentials.password_hash):
            return initial_admin
        else:
            return False
    user = get_user(db, gmail)
    if not user:
        return False
    
    if not user.user_credentials:
        return False
    
    if not verify_password(password, user.user_credentials.password_hash):
        return False
    
    if not user.active:
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.gmail}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> AuthUser:
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
    
    user = get_user(db, gmail=token_data.username)
    if user is None:
        raise credentials_exception
    
    return AuthUser(
        user_id=str(user.user_id),
        username=user.gmail,
        email=user.gmail,
        full_name=user.full_name,
        disabled=not user.active,
        is_admin=user.admin
    )

async def get_current_active_user(current_user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user