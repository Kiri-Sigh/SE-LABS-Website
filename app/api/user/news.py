from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from uuid import UUID
from fastapi.responses import Response

from ...dependencies import get_db
from ...model import *
from ...schemas.news_thumbnail import NewsThumbnail, NT01

router = APIRouter(
    prefix="/user/news",
    tags=["news"],
)

@router.get("/thumbnail", response_model=List[NewsThumbnail])
def get_news_thumbnail(
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_db)
):
    news = db.query(News).filter(News.posted == True)
    if laboratory_id:
        news = news.filter(News.lab_id == laboratory_id)
    if research_id:
        news = news.filter(News.research_id == research_id)
    offset = (page - 1) * amount
    news = news.offset(offset).limit(amount).all()
    return [NT01.to_news_thumbnail(news) for news in news]

@router.get("/related_news", response_model=List[NewsThumbnail])
def get_related_news(news_id: UUID, db = Depends(get_db)):
    news = db.query(News).filter(News.news_id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    if news.research_id:
        related_news = db.query(News).filter(News.research_id == news.research_id).limit(3).all()
        return [NT01.to_news_thumbnail(news) for news in related_news]
    elif news.lab_id:
        related_news = db.query(News).filter(News.lab_id == news.lab_id).limit(3).all()
        return [NT01.to_news_thumbnail(news) for news in related_news]
    else:
        related_news = db.query(News).limit(3).all()
        return [NT01.to_news_thumbnail(news) for news in related_news]
    
@router.get("/image-high")
def get_news_image_high(news_id: UUID, db = Depends(get_db)):
    news = db.query(News).filter(News.news_id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return Response(content=news.image_high, media_type="image/jpeg")

@router.get("/image-low")
def get_news_image_low(news_id: UUID, db = Depends(get_db)):
    news = db.query(News).filter(News.news_id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return Response(content=news.image_low, media_type="image/jpeg")