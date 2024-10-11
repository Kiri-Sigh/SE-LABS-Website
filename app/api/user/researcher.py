from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...model import *
from ...schemas.researcher_thumbnail import ResearcherThumbnail

router = APIRouter(
    prefix="/user/researcher",
    tags=["researcher"],
)

@router.get("/thumbnail", response_model=List[ResearcherThumbnail])
def get_researcher_thumbnail(
    laboratory_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_db)
):
    researcher = db.query(Researcher).filter(Researcher.posted == True)
    if laboratory_id:
        researcher = researcher.filter(Researcher.lab_id == laboratory_id)
    offset = (page - 1) * amount
    return researcher.offset(offset).limit(amount).all()

@router.get("/thumbnail/{researcher_id}", response_model=ResearcherThumbnail)
def get_researcher_thumbnail_by_id(researcher_id: UUID, db = Depends(get_db)):
    researcher = db.query(Researcher).filter(Researcher.id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return researcher

@router.get("/image-high")
def get_researcher_image_high(researcher_id: UUID, db = Depends(get_db)):
    researcher = db.query(Researcher).filter(Researcher.id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return researcher.image_high

@router.get("/image-low")
def get_researcher_image_low(researcher_id: UUID, db = Depends(get_db)):
    researcher = db.query(Researcher).filter(Researcher.id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return researcher.image_low