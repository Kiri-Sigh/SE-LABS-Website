from sqlalchemy.orm import Session
from ..models.model import News
from ..schemas.core.news import NewsCreate, NewsDB

def get_news(db: Session, news_id: int) -> NewsDB:
    return db.query(News).filter(News.news_id == news_id).first()

def get_news_list(db: Session, skip: int = 0, limit: int = 100) -> list[NewsDB]:
    return db.query(News).offset(skip).limit(limit).all()

def create_news(db: Session, news: NewsCreate) -> NewsDB:
    db_news = News(**news.model_dump())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

def delete_news(db: Session, news_id: int):
    db.query(News).filter(News.news_id == news_id).delete()
    db.commit()
    return {"message": "News deleted successfully."}