from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from uuid import UUID
from fastapi.responses import Response
from sqlalchemy import case, select
from sqlalchemy.orm import Session
import logging

from dependencies import get_db
from model import *
from schemas.researcher_thumbnail import ResearcherThumbnail, UT01

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

router = APIRouter(
    prefix="/user/researcher",
    tags=["researcher"],
)

@router.get("/thumbnail", response_model=List[ResearcherThumbnail])
def get_researcher_thumbnail(
    laboratory_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    # Build base query
    query = select(Researcher)
    
    # Add laboratory filter if specified
    if laboratory_id:
        query = (
            query
            .join(Researcher.labs)
            .filter(Laboratory.lab_id == laboratory_id)
        )
        
    query = query.filter(Researcher.highest_role != Position.Admin)
    
    # Define position-based ordering
    position_order = case(
        (Researcher.highest_role == Position.LeadResearcher, 1),
        (Researcher.highest_role == Position.Admin, 2),
        (Researcher.highest_role == Position.Researcher, 3),
        else_=4
    )
    
    # Apply ordering and pagination
    query = query.order_by(position_order)
    offset = (page - 1) * amount
    
    # Log the query
    logging.debug(f"Generated Query: {query}")
    
    # Execute query
    researchers = db.execute(query.offset(offset).limit(amount)).scalars().all()
    
    # Log the results
    logging.debug(f"Query Results: {researchers}")
    
    # Convert to thumbnails
    return [UT01.to_researcher_thumbnail(researcher) for researcher in researchers]

@router.get("/thumbnail/{researcher_id}", response_model=ResearcherThumbnail)
def get_researcher_thumbnail_by_id(researcher_id: UUID, db: Session = Depends(get_db)):
    researcher = db.query(Researcher).filter(Researcher.user_id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return UT01.to_researcher_thumbnail(researcher)

@router.get("/image-high")
def get_researcher_image_high(researcher_id: UUID, db: Session = Depends(get_db)):
    researcher = db.query(Researcher).filter(Researcher.user_id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return Response(content=researcher.image_high, media_type="image/jpeg")

@router.get("/image-low")
def get_researcher_image_low(researcher_id: UUID, db: Session = Depends(get_db)):
    researcher = db.query(Researcher).filter(Researcher.user_id == researcher_id).first()
    if not researcher:
        raise HTTPException(status_code=404, detail="Researcher not found")
    return Response(content=researcher.image_low, media_type="image/jpeg")