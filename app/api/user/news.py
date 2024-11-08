from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import Response

from ...dependencies import get_db
from ...model import *
from ...schemas.news_thumbnail import NewsThumbnail, NT01
from ...crud.news import read_news

router = APIRouter(
    prefix="/user/news",
    tags=["news"],
)

@router.get("/thumbnail", response_model=List[NewsThumbnail])
def get_news_thumbnail_API(
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    news: List[News] = read_news(
        db=db,
        amount=amount,
        page=page,
        laboratory_id=laboratory_id,
        research_id=research_id
    )

    return [NT01.to_news_thumbnail(news) for news in news]

@router.get("/thumbnail/{news_id}", response_model=NewsThumbnail)
def get_news_thumbnail_by_id_API(news_id: UUID, db: Session = Depends(get_db)):
    event: Event = read_news(
        db=db,
        amount=1,
        page=1,
        news_id=news_id
    )[0]
    return NT01.to_news_thumbnail(event)

@router.get("/related_news", response_model=List[NewsThumbnail])
def get_related_news_API(news_id: UUID, db = Depends(get_db)):
    news: News = read_news(
        db=db,
        news_id=news_id
    )[0]
    news_from_research = read_news(
        db=db,
        amount=5,
        page=1,
        research_id=news.research_id
    )
    news_from_laboratory = read_news(
        db=db,
        amount=5,
        page=1,
        laboratory_id=news.lab_id
    )
    related_news = list(set(news_from_research + news_from_laboratory))

    return [NT01.to_news_thumbnail(news) for news in related_news]
    
@router.get("/image-high")
def get_news_image_high_API(news_id: UUID, db: Session = Depends(get_db)):
    news: News = read_news(
        db=db,
        amount=1,
        page=1,
        news_id=news_id
    )[0]
    return Response(content=news.image_high, media_type="image/jpeg")

@router.get("/image-low")
def get_news_image_low_API(news_id: UUID, db: Session = Depends(get_db)):
    news: News = read_news(
        db=db,
        amount=1,
        page=1,
        news_id=news_id
    )[0]
    return Response(content=news.image_low, media_type="image/jpeg")