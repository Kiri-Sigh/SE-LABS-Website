from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session

from ...dependency.database import get_db
from ...schemas.response.news.NT01_news_thumbmail import NT01
from ...schemas.response.news.NIMG01_news_image import NIMG01
from ...models.model import News

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
    news = db.query(News).filter(News.posted == True)
    if laboratory_id:
        news = news.filter(News.lab_id == laboratory_id)
    if research_id:
        news = news.filter(News.research_id == research_id)
    offset = (page - 1) * amount
    news = news.offset(offset).limit(amount).all()
    return [NT01(news) for news in news]


@router.get("/related_news", response_model=list[NT01])
async def get_related_news(
        news_id: str,
        db: Session = Depends(get_db)
        ):
    if (news := db.query(News).filter(News.id == news_id).first()):
        if (news.lab_id):
            related_news = db.query(News).filter(News.lab_id == news.lab_id).limit(3).all()
            return [NT01(news) for news in related_news]
        elif (news.research_id):
            related_news = db.query(News).filter(News.research_id == news.research_id).limit(3).all()
            return [NT01(news) for news in related_news]
        else:
            return db.query(News).limit(3).all()
    else: 
        raise HTTPException(status_code=404, detail="News not found")


@router.get("/image-high", response_model=NIMG01)
async def get_news_image_high(
        news_id: str,
        db: Session = Depends(get_db)
        ):
    if (news := db.query(News).filter(News.id == news_id).first()):
        return NIMG01(news)
    else:
        raise HTTPException(status_code=404, detail="News not found")

@router.get("/image-low", response_model=NIMG01)
async def get_news_image_low(
        news_id: str,
        db: Session = Depends(get_db)
        ):
    if (news := db.query(News).filter(News.id == news_id).first()):
        return NIMG01(news)
    else:
        raise HTTPException(status_code=404, detail="News not found")