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
from .schemas.auth_user import  AuthUser, TokenData, Token, AU01
from .dependencies import get_db
from .schemas.ult.position import Position

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

def create_user(db: Session, user_data: dict, password: str) -> Researcher:
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

def authenticate_user(db: Session, gmail: str, password: str) -> Union[Researcher, bool]:
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
        data={
            "sub": user.gmail,
        }, 
        expires_delta=access_token_expires
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
    # use researcher relation to obtain related_lab, related_research
    return AuthUser(Researcher=AU01.from_orm(user, token))

async def get_current_active_user(current_user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if current_user.Researcher.active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_researcher(research_id: UUID, current_user: AuthUser = Depends(get_current_active_user)) -> AuthUser:
    if research_id not in [research.RID for research in current_user.Researcher.Researches]:
        raise HTTPException(status_code=400, detail=f"User don't have enough permisstion for research: {research_id}")
    return current_user

async def get_current_active_lead_researcher(laboratory_id: UUID, current_user: AuthUser = Depends(get_current_active_user)) -> AuthUser:
    if laboratory_id not in [lab.LID for lab in current_user.Researcher.Laboratories]:
        raise HTTPException(status_code=400, detail=f"User don't have enough permisstion for laboratory: {laboratory_id}")
    return current_user

async def get_current_active_admin(current_user: AuthUser = Depends(get_current_active_user)) -> AuthUser:
    if current_user.Researcher.position != Position.Admin:
        raise HTTPException(status_code=400, detail=f"User don't have enough permisstion you are just {current_user.Researcher.position}")
    return current_user