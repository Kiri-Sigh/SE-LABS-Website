from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from ...dependency.database import get_db
from ...pydantic.response.news.NT01_news_thumbmail import NT01
from ...pydantic.response.news.NIMG01_news_image import NIMG01

router = APIRouter(
    prefix="/user/news",
    tags=["news"],
)

@router.get("/thumbnail", response_model=list[NT01])
async def get_news_thumbnail(
        laboratory_id: Optional[str] = None,
        research_id: Optional[str] = None,
        amount: Optional[int] = 0,
        page: Optional[int] = 1,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get news thumbnail"}

@router.get("/related_news", response_model=list[NT01])
async def get_related_news(
        news_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get related news"}

@router.get("/image-high", response_model=NIMG01)
async def get_news_image_high(
        news_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get news image high"}

@router.get("/image-low", response_model=NIMG01)
async def get_news_image_low(
        news_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get news image low"}