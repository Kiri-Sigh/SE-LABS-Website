from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.request.researcher.readable import ResearcherCreate as readable
from ...dependency.database import get_db

router = APIRouter(
    prefix="/lead-researcher/researcher",
    tags=["researcher"],
)

@router.post("/")
async def create_researcher_and_assign_to_research(
    body: readable.ResearcherCreate,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Researcher created"}

@router.patch("/")
async def assign_to_research(
    researcher_id: int,
    research_id: int,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Researcher updated"}

@router.delete("/")
async def delete_researcher_out_of_research(
    researcher_id: int,
    research_id: int,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Researcher deleted"}