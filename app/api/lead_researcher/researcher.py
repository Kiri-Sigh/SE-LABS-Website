from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from pydantic import EmailStr
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...auth import get_current_user
from ...model import *

router = APIRouter(
    prefix="/lead_researcher/researcher",
    tags=["researcher"],
)

@router.post("/")
def create_researcher(
    name: str,
    email: EmailStr,
    password: str,
    image: UploadFile = File(...),
    db = Depends(get_db),
    user = Depends(get_current_user)
):
    researcher = Researcher(name=name, email=email)
    researcher.set_password(password)
    db.add(researcher)
    db.commit()
    return researcher