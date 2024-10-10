from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from ...dependency.database import get_db
from ...dependency.get_current_user import get_current_user
from ...models.model import Person, UserCredentials
from ...schemas.request.researcher.readable import ResearcherLogin as readable
from ...token.token import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="/researcher/researcher",
    tags=["researcher"],
)

@router.get("/info/{researcher_id}")
async def get_researcher_info(
    researcher_id: int,
    current_user: Person = Depends(get_current_user),
    db: Session = Depends(get_db)
        ):
    researcher = db.query(Person).filter(Person.id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return researcher

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
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
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auto-login")
async def auto_login(
    current_user: Person = Depends(get_current_user),
    db: Session = Depends(get_db)
        ):
    researcher = db.query(UserCredentials).filter(UserCredentials.username == current_user.username).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    if researcher.password != current_user.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"message": "Researcher logged in"}