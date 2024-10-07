from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.request.researcher.readable import ResearcherLogin as readable
from ...dependency.database import get_db

router = APIRouter(
    prefix="/researcher/researcher",
    tags=["researcher"],
)

@router.get("/info/{researcher_id}")
async def get_researcher_info(
    researcher_id: int,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Researcher info returned"}

@router.post("/login")
async def login(
    body: readable.ResearcherLogin,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Researcher logged in"}

@router.post("/auto-login")
async def auto_login(
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Researcher auto-logged in"}