from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...dependency.database import get_db
from ...dependency.get_current_user import get_current_user
from ...models.model import Person, UserCredentials
from ...schemas.request.researcher.readable import ResearcherLogin as readable

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
async def login(
    body: readable.ResearcherLogin,
    current_user: Person = Depends(get_current_user),
    db: Session = Depends(get_db)
        ):
    researcher = db.query(UserCredentials).filter(UserCredentials.username == body.username).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    if researcher.password != body.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"message": "Researcher logged in"}

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