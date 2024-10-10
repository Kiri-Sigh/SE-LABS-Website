from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...auth import get_current_user
from ...model import *

router = APIRouter(
    prefix="/researcher/researcher",
    tags=["researcher"],
)

@router.get("/info/{researcher_id}")
def get_researcher_info(
    researcher_id: UUID, 
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    researcher = db.query(Researcher).filter(Researcher.id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return researcher

@router.post("/login")
def researcher_login(
    gmail: str,
    password: str,
    db = Depends(get_db),
):
    researcher = db.query(Researcher).filter(Researcher.email == gmail).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    if not researcher.check_password(password):
        raise HTTPException(status_code=401, detail="Invalid password")
    return researcher

@router.post("/auto_login")
def researcher_auto_login(
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return current_user