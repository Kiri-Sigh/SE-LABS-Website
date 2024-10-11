from fastapi import APIRouter

from .event import router as event_router
from .laboratory import router as laboratory_router
from .news import router as news_router
from .publication import router as publication_router
from .research import router as research_router
from .researcher import router as researcher_router

router = APIRouter()
router.include_router(event_router)
router.include_router(laboratory_router)
router.include_router(news_router)
router.include_router(publication_router)
router.include_router(research_router)
router.include_router(researcher_router)