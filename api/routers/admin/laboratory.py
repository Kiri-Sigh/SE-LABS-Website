from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.request.laboratory.readable import LaboratoryCreate as readable
from ...dependency.database import get_db

router = APIRouter(
    prefix="/admin/laboratory",
    tags=["laboratory"],
)

@router.post("/")
async def create_laboratory(
    body: readable.LaboratoryCreate,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Laboratory created"}

@router.delete("/")
async def delete_laboratory(
    laboratory_id: int,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Laboratory deleted"}