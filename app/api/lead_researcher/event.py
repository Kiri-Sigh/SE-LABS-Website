from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...model import *
from ...auth import get_current_active_lead_researcher
from ...schemas.auth_user import AuthUser
from ...schemas.event_thumbnail import EventThumbnail, ET01

router = APIRouter(
    prefix="/lead_researcher/event",
    tags=["event"],
)

@router.get("/commit", response_model=List[EventThumbnail])
def get_commit_events(
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    events = db.query(Event).filter(Event.posted == False)
    if laboratory_id:
        events = events.filter(Event.lab_id == laboratory_id)
    if research_id:
        events = events.filter(Event.research_id == research_id)
    offset = (page - 1) * amount
    events = events.offset(offset).limit(amount).all()
    return [ET01.to_event_thumbnail(event) for event in events]

@router.patch("/", response_model=EventThumbnail)
def change_event_post_stage(
    event_id: UUID,
    is_approved: bool = Query(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event.posted = is_approved
    db.commit()
    return ET01.to_event_thumbnail(event)

@router.delete("/", response_model=EventThumbnail)
def delete_event(
    event_id: UUID,
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    result = ET01.to_event_thumbnail(event)
    db.delete(event)
    db.commit()
    return result