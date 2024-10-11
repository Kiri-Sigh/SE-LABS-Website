from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...model import *
from ...schemas.news_thumbnail import NewsThumbnail

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
    return news.offset(offset).limit(amount).all()

@router.get("/related_news", response_model=List[NewsThumbnail])
def get_related_news(news_id: UUID, db = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    if news.research_id:
        related_news = db.query(News).filter(News.research_id == news.research_id).limit(3).all()
        return related_news
    elif news.lab_id:
        related_news = db.query(News).filter(News.lab_id == news.lab_id).limit(3).all()
        return related_news
    else:
        return db.query(News).limit(3).all()
    
@router.get("/image-high")
def get_news_image_high(news_id: UUID, db = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news.image_high

@router.get("/image-low")
def get_news_image_low(news_id: UUID, db = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news.image_low