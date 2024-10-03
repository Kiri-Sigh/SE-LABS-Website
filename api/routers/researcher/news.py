from fastapi import APIRouter, Body

from ...schemas.request.news.readable import NewsCreate as schema

router = APIRouter(
    prefix="/researcher/news",
    tags=["news"],
)

@router.post("/")
async def create_news(
    body: schema.NewsCreate = Body(...)
        ):
    return {"message": "News posted"}