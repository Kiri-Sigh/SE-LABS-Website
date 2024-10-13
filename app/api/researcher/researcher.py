from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...auth import get_current_active_user
from ...model import *
from ...schemas.auth_user import AuthUser
from ...schemas.researcher_thumbnail import ResearcherThumbnail, UT01

router = APIRouter(
    prefix="/researcher/researcher",
    tags=["researcher"],
)

@router.post("/auto_login", response_model=AuthUser)
def researcher_auto_login(
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_user)
):
    return current_user