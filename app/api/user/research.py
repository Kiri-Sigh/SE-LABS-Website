from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...model import *
from ...schemas.research_thumbnail import ResearchThumbnail

router = APIRouter(
    prefix="/user/research",
    tags=["research"],
)

@router.get("/thumbnail", response_model=List[ResearchThumbnail])
def get_research_thumbnail(
    laboratory_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_db)
):
    research = db.query(Research).filter(Research.posted == True)
    if laboratory_id:
        research = research.filter(Research.lab_id == laboratory_id)
    offset = (page - 1) * amount
    return research.offset(offset).limit(amount).all()

@router.get("/thumbnail/{research_id}", response_model=ResearchThumbnail)
def get_research_thumbnail_by_id(research_id: UUID, db = Depends(get_db)):
    research = db.query(Research).filter(Research.id == research_id).first()
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    return research

@router.get("/image-high")
def get_research_image_high(research_id: UUID, db = Depends(get_db)):
    research = db.query(Research).filter(Research.id == research_id).first()
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    return research.image_high

@router.get("/image-low")
def get_research_image_low(research_id: UUID, db = Depends(get_db)):
    research = db.query(Research).filter(Research.id == research_id).first()
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    return research.image_low