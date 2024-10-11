from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...model import *
from ...schemas.event_thumbnail import EventThumbnail

router = APIRouter(
    prefix="/user/event",
    tags=["event"],
)

@router.get("/thumbnail", response_model=List[EventThumbnail])
def get_event_thumbnail(
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_db)
):
    event = db.query(Event).filter(Event.posted == True)
    if laboratory_id:
        event = event.filter(Event.lab_id == laboratory_id)
    if research_id:
        event = event.filter(Event.research_id == research_id)
    offset = (page - 1) * amount
    return event.offset(offset).limit(amount).all()
    

@router.get("/image-high")
def get_event_image_high(event_id: UUID, db = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event.image_high

@router.get("/image-low")
def get_event_image_low(event_id: UUID, db = Depends(get_db)):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event.image_low