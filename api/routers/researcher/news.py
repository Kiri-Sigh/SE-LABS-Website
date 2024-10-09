from fastapi import APIRouter, Body, Header, Depends

from ...schemas.request.news.readable import NewsCreate as schema
from ...dependency.get_current_user import get_current_user
from ...dependency.database import get_db
from ...models.model import News, person_lab, person_research, Person

router = APIRouter(
    prefix="/researcher/news",
    tags=["news"],
)

@router.post("/", response_model=schema.NewsCreate)
async def create_news(
    body: schema.NewsCreate = Body(...),
    current_user: Person = Depends(get_current_user),
    db = Depends(get_db)
        ):
    news = News(
        title=body.title,
        body=body.body,
        lab_id=body.lab_id,
        research_id=body.research_id,
        posted=body.posted,
        image_high=body.image_high
    )
    db.add(news)
    db.commit()
    db.refresh(news)
    return news
