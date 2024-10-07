from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from ..models.model import News
from ..schemas.core.news import NewsCreate, NewsDB

async def get_news(db: AsyncSession, news_id: int) -> NewsDB:
    try:
        result = await db.execute(select(News).filter(News.news_id == news_id))
        news = result.scalars().first()
        if not news:
            raise HTTPException(status_code=404, detail="News not found")
        return news
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_news_list(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[NewsDB]:
    try:
        result = await db.execute(select(News).offset(skip).limit(limit))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def create_news(db: AsyncSession, news: NewsCreate) -> NewsDB:
    try:
        db_news = News(**news.model_dump())
        db.add(db_news)
        await db.commit()
        await db.refresh(db_news)
        return db_news
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_news(db: AsyncSession, news_id: int) -> dict:
    try:
        result = await db.execute(select(News).filter(News.news_id == news_id))
        news = result.scalars().first()
        if not news:
            raise HTTPException(status_code=404, detail="News not found")
        await db.delete(news)
        await db.commit()
        return {"message": "News deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")