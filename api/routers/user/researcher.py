from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from ...dependency.database import get_db
from ...pydantic.response.researcher.UT01_researcher_thumbnail import RT01
from ...pydantic.response.researcher.UIMG01_researcher_image import UIMG01

router = APIRouter(
    prefix="/user/researcher",
    tags=["researcher"],
)

@router.get("/thumbnail", list[RT01])
async def get_researcher_thumbnail(
        laboratory_id: Optional[str] = None,
        research_id: Optional[str] = None,
        amount: Optional[int] = 0,
        page: Optional[int] = 1,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get researcher thumbnail"}

@router.get("/image-high", response_model=UIMG01)
async def get_researcher_image_high(
        researcher_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get researcher image high"}

@router.get("/image-low", response_model=UIMG01)
async def get_researcher_image_low(
        researcher_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get researcher image low"}