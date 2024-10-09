from fastapi import APIRouter, Header, Depends, HTTPException

from ...dependency.get_current_user import get_current_user
from ...dependency.database import get_db
from ...schemas.request.news.readable import NewsCreate as schema
from ...models.model import News, Person

router = APIRouter(
    prefix="/lead-researcher/news",
    tags=["news"],
)

@router.get("/commit")
async def get_commit(
    laboratory_id: int,
    current_user: Person = Depends(get_current_user),
    db = Depends(get_db)
        ):
    news = db.query(News).filter(News.posted == False)
    if laboratory_id:
        news = news.filter(News.lab_id == laboratory_id)
    return news.all()

@router.patch("/")
async def update_news(
    news_id: int,
    approve: bool,
    current_user: Person = Depends(get_current_user),
    db = Depends(get_db)
        ):
    news = db.query(News).filter(News.news_id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    news.posted = approve
    db.commit()
    db.refresh(news)
    return news
    

@router.delete("/")
async def delete_news(
    news_id: int,
    current_user: Person = Depends(get_current_user),
    db = Depends(get_db)
        ):
    news = db.query(News).filter(News.news_id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    db.delete(news)
    db.commit()
    return news