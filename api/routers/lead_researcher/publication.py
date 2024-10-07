from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.request.publication.readable import PublicationUpdate as readable
from ...dependency.database import get_db

router = APIRouter(
    prefix="/lead-researcher/publication",
    tags=["publication"],
)

@router.patch("/")
async def update_publication(
    publication_id: int,
    body: readable.PublicationUpdate,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Publication updated"}

@router.delete("/")
async def delete_publication(
    publication_id: int,
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "Publication deleted"}