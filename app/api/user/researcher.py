from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from uuid import UUID
from fastapi.responses import Response

from ...dependencies import get_db
from ...model import *
from ...schemas.researcher_thumbnail import ResearcherThumbnail, UT01

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
    researcher = db.query(Researcher)
    if laboratory_id:
        researcher = researcher.filter(Researcher.user_id == laboratory_id)
    offset = (page - 1) * amount
    researchers = researcher.offset(offset).limit(amount).all()
    return [UT01.to_researcher_thumbnail(researcher) for researcher in researchers]

@router.get("/thumbnail/{researcher_id}", response_model=ResearcherThumbnail)
def get_researcher_thumbnail_by_id(researcher_id: UUID, db = Depends(get_db)):
    researcher = db.query(Researcher).filter(Researcher.user_id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return UT01.to_researcher_thumbnail(researcher)

@router.get("/image-high")
def get_researcher_image_high(researcher_id: UUID, db = Depends(get_db)):
    researcher = db.query(Researcher).filter(Researcher.user_id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return Response(content=researcher.image_high, media_type="image/jpeg")

@router.get("/image-low")
def get_researcher_image_low(researcher_id: UUID, db = Depends(get_db)):
    researcher = db.query(Researcher).filter(Researcher.user_id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return Response(content=researcher.image_low, media_type="image/jpeg")