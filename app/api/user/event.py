from fastapi.responses import Response
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from schemas.event_thumbnail import EventThumbnail, ET01
from crud.event import read_event
from model import Event
from dependencies import get_db

router = APIRouter(
    prefix="/user/event",
    tags=["event"],
)

@router.get("/thumbnail", response_model=list[EventThumbnail])
def get_event_thumbnail_API(
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):  
    events: List[Event] = read_event(
        db=db,
        amount=amount,
        page=page,
        laboratory_id=laboratory_id,
        research_id=research_id
    )
    return [ET01.to_event_thumbnail(event) for event in events]

@router.get("/thumbnail/{event_id}", response_model=EventThumbnail)
def get_event_thumbnail_by_id_API(event_id: UUID, db: Session = Depends(get_db)):
    event: Event = read_event(
        db=db,
        amount=1,
        page=1,
        event_id=event_id
    )[0]
    return ET01.to_event_thumbnail(event)
    

@router.get("/image-high")
def get_event_image_high_API(event_id: UUID, db: Session = Depends(get_db)):
    event: Event = read_event(
        db=db,
        amount=1,
        page=1,
        event_id=event_id
    )[0]
    return Response(content=event.image_high, media_type="image/jpeg")

@router.get("/image-low")
def get_event_image_low_API(event_id: UUID, db: Session = Depends(get_db)):
    event: Event = read_event(
        db = db,
        amount=1,
        page=1,
        event_id=event_id
    )[0]
    return Response(content=event.image_low, media_type="image/jpeg")