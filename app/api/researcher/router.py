from fastapi import APIRouter

from .researcher import router as researcher_router
from .news import router as news_router
from .event import router as event_router

router = APIRouter()
router.include_router(researcher_router)
router.include_router(news_router)
router.include_router(event_router)