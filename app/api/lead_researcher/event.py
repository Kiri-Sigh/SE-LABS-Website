from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from uuid import UUID

from dependencies import get_db
from model import Event
from auth import get_current_active_authorized_user
from schemas.auth_user import AuthUser
from schemas.event_thumbnail import EventThumbnail, ET01
from crud.event import read_event, update_event_post_stage, delete_event

router = APIRouter(
    prefix="/lead_researcher/event",
    tags=["event"],
)

@router.get("/commit", response_model=List[EventThumbnail])
def get_commit_events_API(
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    current_user: AuthUser = Depends(get_current_active_authorized_user),
    db = Depends(get_db)
):
    events: List[Event] = read_event(
        db=db,
        posted=False,
        amount=amount,
        page=page,
        laboratory_id=laboratory_id,
        research_id=research_id
    )
    return [ET01.to_event_thumbnail(event) for event in events]

@router.patch("/", response_model=EventThumbnail)
def change_event_post_stage_API(
    event_id: UUID,
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    is_approved: bool = Query(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_authorized_user)
):
    event: Event = update_event_post_stage(event_id=event_id, is_approved=is_approved, db=db, laboratory_id=laboratory_id, research_id=research_id)
    return ET01.to_event_thumbnail(event)

@router.delete("/", response_model=None)
def delete_events_API(
    event_id: UUID,
    laboratory_id: Optional[UUID] = Query(None),
    research_id: Optional[UUID] = Query(None),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_authorized_user)
):
    result = delete_event(event_id=event_id, db=db, laboratory_id=laboratory_id, research_id=research_id)
    return result