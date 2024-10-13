from fastapi import APIRouter

from .researcher import router as researcher_router
from .laboratory import router as laboratory_router

router = APIRouter()
router.include_router(researcher_router)
router.include_router(laboratory_router)