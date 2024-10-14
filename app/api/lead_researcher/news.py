from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...model import *
from ...auth import get_current_active_lead_researcher
from ...schemas.auth_user import AuthUser
from ...schemas.news_thumbnail import NewsThumbnail, NT01

router = APIRouter(
    prefix="/lead_researcher/news",
    tags=["news"],
)

@router.get("/commit", response_model=List[NewsThumbnail])
def get_commit_news(
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    news = db.query(News).filter(News.posted == False)
    if laboratory_id:
        news = news.filter(News.lab_id == laboratory_id)
    if research_id:
        news = news.filter(News.research_id == research_id)
    offset = (page - 1) * amount
    news = news.offset(offset).limit(amount).all()
    return [NT01.to_news_thumbnail(news) for news in news]

@router.patch("/", response_model=NewsThumbnail)
def change_news_post_stage(
    news_id: UUID,
    is_approved: bool = Query(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    news = db.query(News).filter(News.news_id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    news.posted = is_approved
    db.commit()
    return NT01.to_news_thumbnail(news)

@router.delete("/", response_model=NewsThumbnail)
def delete_news(
    news_id: UUID,
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    news = db.query(News).filter(News.news_id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    result = NT01.to_news_thumbnail(news)
    db.delete(news)
    db.commit()
    return result