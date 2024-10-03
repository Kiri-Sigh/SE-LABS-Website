from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from ...dependency.database import get_db
from ...schemas.response.research.RT01_research_thumbnail import RT01
from ...schemas.response.research.RIMG01_research_image import RIMG01

router = APIRouter(
    prefix="/user/research",
    tags=["research"],
)

@router.get("/thumbnail", response_model=list[RT01])
async def get_research_thumbnail(
        laboratory_id: Optional[str] = None,
        amount: Optional[int] = 0,
        page: Optional[int] = 1,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get research thumbnail"}

@router.get("/thumbnail/{research_id}", response_model=RT01)
async def get_research_detail(
        research_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get research detail"}

@router.get("/image-high", response_model=RIMG01)
async def get_research_image_high(
        research_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get research image high"}

@router.get("/image-low", response_model=RIMG01)
async def get_research_image_low(
        research_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get research image low"}