from fastapi import APIRouter

from .user.router import router as user_router
from .researcher.router import router as researcher_router
from .lead_researcher.router import router as lead_researcher_router
from .admin.router import router as admin_router

router = APIRouter()
router.include_router(user_router)
router.include_router(researcher_router)
router.include_router(lead_researcher_router)
router.include_router(admin_router)