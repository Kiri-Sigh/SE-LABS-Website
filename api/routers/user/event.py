from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID

from ...dependency.database import get_db
from ...schemas.response.event.RET01_response_event_thumbnail import RET01
from ...schemas.response.event.ET01_event_thumbnail import ET01
from ...schemas.response.event.EIMGH01_event_image_high import EIMGH01
from ...schemas.response.event.EIMGL01_event_image_low import EIMGL01
from ...schemas.util.ImageResponse import ImageResponse
from ...models import model as models

router = APIRouter(
    prefix="/user/event",
    tags=["event"],
)

@router.get("/thumbnail", response_model=list[RET01])
async def get_event_thumbnail(
        laboratory_id: Optional[UUID] = Query(None, description="Filter by laboratory ID"),
        research_id: Optional[UUID] = Query(None, description="Filter by research ID"),
        amount: int = Query(10, ge=1, le=100, description="Number of events to return"),
        page: int = Query(1, ge=1, description="Page number"),
        db: Session = Depends(get_db)
        ):
    query = db.query(models.Event).filter(models.Event.posted == True)
    if laboratory_id:
        query = query.filter(models.Event.lab_id == laboratory_id)
    if research_id:
        query = query.filter(models.Event.research_id == research_id)
    offset = (page - 1) * amount
    events = query.offset(offset).limit(amount).all()
    return [RET01(Event=ET01.model_validate(event)) for event in events]

@router.get("/image-high", response_model=ImageResponse)
async def get_event_image_high(
        event_id: UUID,
        db: Session = Depends(get_db)
        ):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if not event.image_high:
        raise HTTPException(status_code=404, detail="High resolution image not found for this event")
    return ImageResponse(image=EIMGH01.from_orm(event))

@router.get("/image-low", response_model=ImageResponse)
async def get_event_image_low(
        event_id: UUID,
        db: Session = Depends(get_db)
        ):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if not event.image_low:
        raise HTTPException(status_code=404, detail="Low resolution image not found for this event")
    return ImageResponse(image=EIMGL01.from_orm(event))