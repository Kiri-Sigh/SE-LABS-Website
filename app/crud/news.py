from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import Tuple, Optional, List
from uuid import UUID
from schemas.news_io import NewsCreate
from dependencies import process_image
from model import News

async def create_news(news: NewsCreate, image: UploadFile, db: Session,
                      research_id: Optional[UUID] = None, laboratory_id: Optional[UUID] = None
                      ) -> News:
    processed_images: Tuple[bytes, bytes] = await process_image(image)
    high_res: bytes = processed_images[0]
    low_res: bytes = processed_images[1]
    related_laboratory = None
    related_research = None

    if news.related_laboratory is not None:
        related_laboratory = news.related_laboratory.LID
    if news.related_laboratory is not None and news.related_laboratory.related_research is not None:
        related_research = news.related_laboratory.related_research.RID

    if laboratory_id != related_laboratory:
        if laboratory_id is not None:
            raise HTTPException(status_code=400, detail="Laboratory ID in NewsCreate and in scope mismatch")
    if research_id != related_research:
        raise HTTPException(status_code=400, detail="Research ID in NewsCreate and in scope mismatch")
    
    new_news = News(
        news_name=news.title,
        image_high=high_res,
        image_low=low_res,
        body=news.body,
        posted=False,
        lab_id=related_laboratory,
        research_id=related_research
    )

    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    return new_news

def read_news(db: Session, posted: bool = True,
              amount: int = 10, page: int = 1,
              research_id: Optional[UUID] = None,
              laboratory_id: Optional[UUID] = None,
              news_id: Optional[UUID] = None, ) -> List[News]:
    news = db.query(News).filter(News.posted == posted)
    if laboratory_id:
        news = news.filter(News.lab_id == laboratory_id)
    if research_id:
        news = news.filter(News.research_id == research_id)
    if news_id:
        news = news.filter(News.news_id == news_id)
    news = news.order_by(News.date.desc())
    offset = (page - 1) * amount
    news = news.offset(offset).limit(amount).all()
    if not news:
        raise HTTPException(status_code=404, detail="No news found")
    return news

async def update_news(db: Session, news_id: UUID, news_param: NewsCreate, image: UploadFile,
                laboratory_id: Optional[UUID] = None, research_id: Optional[UUID] = None) -> News:
    process_images: Tuple[bytes, bytes] = await process_image(image)
    high_res: bytes = process_images[0]
    low_res: bytes = process_images[1]
    related_laboratory = None
    related_research = None

    if news_param.related_laboratory is not None:
        related_laboratory = news_param.related_laboratory.LID
        if news_param.related_laboratory.related_research is not None:
            related_research = news_param.related_laboratory.related_research.RID

    if laboratory_id != related_laboratory:
        if laboratory_id is not None:
            raise HTTPException(status_code=400, detail="Laboratory ID in NewsCreate and in scope mismatch")
    if research_id != related_research:
        raise HTTPException(status_code=400, detail="Research ID in NewsCreate and in scope mismatch")

    news = db.query(News)
    news = news.filter(News.news_id == news_id)
    if laboratory_id:
        news = news.filter(News.lab_id == laboratory_id)
    if research_id:
        news = news.filter(News.research_id == research_id)
    news = news.first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    news.news_name = news_param.title
    news.image_high = high_res
    news.image_low = low_res
    news.body = news_param.body
    news.lab_id = related_laboratory
    news.research_id = related_research

    db.commit()
    return read_news(db, news_id=news_id)[0]

def update_news_post_stage(db: Session, news_id: UUID, posted: bool,
                        laboratory_id: Optional[UUID] = None, research_id: Optional[UUID] = None) -> News:
    news = db.query(News)
    news = news.filter(News.news_id == news_id)
    if laboratory_id:
        news = news.filter(News.lab_id == laboratory_id)
    if research_id:
        news = news.filter(News.research_id == research_id)
    news = news.first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    news.posted = posted
    db.commit()
    print("WE ARE HERE")
    return read_news(db, news_id=news_id, posted=posted)[0]

def delete_news(db: Session, news_id: UUID, 
                laboratory_id: Optional[UUID] = None, research_id: Optional[UUID] = None) -> News:
    news = db.query(News).filter(News.news_id == news_id)
    if laboratory_id:
        news = news.filter(News.lab_id == laboratory_id)
    if research_id:
        news = news.filter(News.research_id == research_id)
    news = news.first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    db.delete(news)
    db.commit()
    return None