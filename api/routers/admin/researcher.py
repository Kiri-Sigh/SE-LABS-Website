from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...dependency.database import get_db

router = APIRouter(
    prefix="/admin/researcher",
    tags=["researcher"],
)

@router.patch("/")
async def assign_to_lead_researcher(
    laboratory_id: int,
    researcher_id: int,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Researcher updated"}

@router.delete("/")
async def delete_researcher_out_of_laboratory(
    laboratory_id: int,
    researcher_id: int,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Researcher deleted"}