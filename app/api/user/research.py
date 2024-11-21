from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from uuid import UUID
from fastapi.responses import Response

from ...dependencies import get_db
from ...model import *
from ...schemas.research_thumbnail import ResearchThumbnail, RT01

router = APIRouter(
    prefix="/user/research",
    tags=["research"],
)

@router.get("/thumbnail/{research_id}", response_model=ResearchThumbnail)
def get_research_thumbnail_by_id(research_id: UUID, db = Depends(get_db)):
    research = db.query(Research).filter(Research.research_id == research_id).first()
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    return RT01.to_research_thumbnail(research)

@router.get("/thumbnail", response_model=List[ResearchThumbnail])
def get_research_thumbnail(
    laboratory_id: Optional[UUID] = Query(None),
    researcher_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_db)
):
    research = db.query(Research)
    
    if researcher_id:
        # Find lab IDs where the researcher is a member
        subquery = db.query(person_lab.__table__.c.lab_id)\
            .filter(person_lab.__table__.c.user_id == researcher_id)\
            .subquery()
        
        # Include research from those labs
        research = research.filter(
            Research.lab_id.in_(subquery)
        )
    
    if laboratory_id:
        research = research.filter(Research.lab_id == laboratory_id)
    
    offset = (page - 1) * amount
    researches = research.offset(offset).limit(amount).all()
    return [RT01.to_research_thumbnail(research) for research in researches]


@router.get("/image-high")
def get_research_image_high(research_id: UUID, db = Depends(get_db)):
    research = db.query(Research).filter(Research.research_id == research_id).first()
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    return Response(content=research.image_high, media_type="image/jpeg")

@router.get("/image-low")
def get_research_image_low(research_id: UUID, db = Depends(get_db)):
    research = db.query(Research).filter(Research.research_id == research_id).first()
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    return Response(content=research.image_low, media_type="image/jpeg")