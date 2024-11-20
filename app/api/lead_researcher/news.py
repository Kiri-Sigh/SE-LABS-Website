from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from uuid import UUID

from dependencies import get_db
from model import *
from auth import get_current_active_authorized_user
from schemas.auth_user import AuthUser
from schemas.news_thumbnail import NewsThumbnail, NT01
from crud.news import read_news, update_news_post_stage, delete_news

router = APIRouter(
    prefix="/lead_researcher/news",
    tags=["news"],
)

@router.get("/commit", response_model=List[NewsThumbnail])
def get_commit_news_API(
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_authorized_user)
):
    news: List[News] = read_news(
        db=db,
        posted=False,
        amount=amount,
        page=page,
        laboratory_id=laboratory_id,
        research_id=research_id
    )
    return [NT01.to_news_thumbnail(news) for news in news]

@router.patch("/", response_model=NewsThumbnail)
def change_news_post_stage_API(
    news_id: UUID,
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    is_approved: bool = Query(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_authorized_user)
):
    news: News = update_news_post_stage(news_id=news_id, posted=is_approved, db=db, laboratory_id=laboratory_id, research_id=research_id)
    print("WE ARE HERE")
    return NT01.to_news_thumbnail(news)

@router.delete("/", response_model=None)
def delete_news_API(
    news_id: UUID,
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_authorized_user)
):
    result = delete_news(news_id=news_id, db=db, laboratory_id=laboratory_id, research_id=research_id)
    return result