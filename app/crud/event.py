from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import Tuple, Optional, List
from uuid import UUID
from schemas.event_io import EventCreate
from dependencies import process_image
from model import Event
from sqlalchemy import case
from datetime import datetime

async def create_event(event: EventCreate, image: UploadFile, db: Session,
                research_id: Optional[UUID] = None, laboratory_id: Optional[UUID] = None
                ) -> Event:
    processed_images: Tuple[bytes, bytes] = await process_image(image)
    high_res: bytes = processed_images[0]
    low_res: bytes = processed_images[1]
    related_laboratory = None
    related_research = None

    if event.related_laboratory is not None:
        related_laboratory = event.related_laboratory.LID
    if event.related_laboratory.related_research is not None:
        related_research = event.related_laboratory.related_research.RID
    
    if laboratory_id != related_laboratory:
        if laboratory_id is not None:
            raise HTTPException(status_code=400, detail="Laboratory ID in EventCreate and in scope mismatch")
    if research_id != related_research:
        raise HTTPException(status_code=400, detail="Research ID in EventCreate and in scope mismatch")

    new_event = Event(
        event_name=event.title,
        image_high=high_res,
        image_low=low_res,
        body=event.body,
        location=event.location,
        date_start=event.start,
        date_end=event.end,
        posted=False,
        lab_id=related_laboratory,
        research_id=related_research
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def read_event(db: Session, posted: bool = True, 
               amount: int = 10, page: int = 1, 
               research_id: Optional[UUID] = None,
               laboratory_id: Optional[UUID] = None, 
               event_id: Optional[UUID] = None) -> List[Event]:
    event = db.query(Event).filter(Event.posted == posted)
    if laboratory_id:
        event = event.filter(Event.lab_id == laboratory_id)
    if research_id:
        event = event.filter(Event.research_id == research_id)
    if event_id:
        event = event.filter(Event.event_id == event_id)
    
    now = datetime.now()
    event = event.order_by(
        case(
            (Event.date_end < now, 2),      # Finished events
            (Event.date_start <= now, 0),  # Ongoing events
            (Event.date_start > now, 1),   # Upcoming events
        ),
        Event.date_start.asc()  # Secondary sort by start date
    )
    
    offset = (page - 1) * amount
    events = event.offset(offset).limit(amount).all()
    if not events:
        raise HTTPException(status_code=404, detail="Event not found")
    return events

async def update_event(db: Session, event_id: UUID, event_param: EventCreate, image: UploadFile,
                 laboratory_id: Optional[UUID] = None, research_id: Optional[UUID] = None) -> Event:
    process_images: Tuple[bytes, bytes] = await process_image(image)
    high_res: bytes = process_images[0]
    low_res: bytes = process_images[1]
    related_laboratory = None
    related_research = None

    if event_param.related_laboratory is not None:
        related_laboratory = event_param.related_laboratory.LID
        if event_param.related_laboratory.related_research is not None:
            related_research = event_param.related_laboratory.related_research.RID

    if laboratory_id != related_laboratory:
        if laboratory_id is not None:
            raise HTTPException(status_code=400, detail="Laboratory ID in NewsCreate and in scope mismatch")
    if research_id != related_research:
        raise HTTPException(status_code=400, detail="Research ID in NewsCreate and in scope mismatch")
    
    event = db.query(Event)
    event = event.filter(Event.event_id == event_id)
    if laboratory_id:
        event = event.filter(Event.lab_id == laboratory_id)
    if research_id:
        event = event.filter(Event.research_id == research_id)
    event = event.first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.event_name = event_param.title
    event.image_high = high_res
    event.image_low = low_res
    event.body = event_param.body
    event.location = event_param.location
    event.date_start = event_param.start
    event.date_end = event_param.end
    event.lab_id = related_laboratory
    event.research_id = related_research

    db.commit()
    return read_event(event_id=event_id, db=db)[0]

def update_event_post_stage(db: Session, event_id: UUID, is_approved: bool,
                            laboratory_id: Optional[UUID] = None, research_id: Optional[UUID] = None) -> Event:
    event = db.query(Event)
    event = event.filter(Event.event_id == event_id)
    if laboratory_id:
        event = event.filter(Event.lab_id == laboratory_id)
    if research_id:
        event = event.filter(Event.research_id == research_id)
    event = event.first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.posted = is_approved
    db.commit()
    return read_event(event_id=event_id, db=db, posted=is_approved)[0]

def delete_event(event_id: UUID, db: Session,
                 laboratory_id: Optional[UUID] = None, research_id: Optional[UUID] = None
                 ) -> None:
    event = db.query(Event).filter(Event.event_id == event_id)
    if laboratory_id:
        event = event.filter(Event.lab_id == laboratory_id)
    if research_id:
        event = event.filter(Event.research_id == research_id)
    event = event.first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return None