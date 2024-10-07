from fastapi import APIRouter, Body, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...schemas.request.news.readable import NewsCreate as schema
from ...dependency.database import get_db

router = APIRouter(
    prefix="/researcher/news",
    tags=["news"],
)

@router.post("/")
async def create_news(
    body: schema.NewsCreate = Body(...),
    token: str = Header(),
    db: AsyncSession = Depends(get_db)
        ):
    return {"message": "News posted"}