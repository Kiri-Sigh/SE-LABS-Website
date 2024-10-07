from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.request.laboratory.readable import LaboratoryUpdate as readable
from ...dependency.database import get_db

router = APIRouter(
    prefix="/lead-researcher/laboratory",
    tags=["laboratory"],
)

@router.patch("/")
async def update_laboratory(
    laboratory_id: int,
    body: readable.LaboratoryUpdate,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Laboratory updated"}