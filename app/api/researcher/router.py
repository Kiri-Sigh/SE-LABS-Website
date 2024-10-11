from fastapi import APIRouter

from .researcher import router as researcher_router

router = APIRouter()
router.include_router(researcher_router)