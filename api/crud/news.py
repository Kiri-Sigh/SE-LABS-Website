from sqlalchemy.ext.asyncio import AsyncSession

from ..models.model import News
from ..schemas.core.news import NewsCreate, NewsDB

async def get_news(db: AsyncSession, news_id: int) -> NewsDB:
    # return db.query(News).filter(News.news_id == news_id).first()
    return db.execute(db.query(News).filter(News.news_id == news_id)).scalars().first()

async def get_news_list(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[NewsDB]:
    # return db.query(News).offset(skip).limit(limit).all()
    return db.execute(db.query(News).offset(skip).limit(limit)).scalars().all()

async def create_news(db: AsyncSession, news: NewsCreate) -> NewsDB:
    db_news = News(**news.model_dump())
    await db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    return db_news

async def delete_news(db: AsyncSession, news_id: int):
    # db.query(News).filter(News.news_id == news_id).delete()
    await db.execute(db.query(News).filter(News.news_id == news_id)).delete()
    await db.commit()
    return {"message": "News deleted successfully."}