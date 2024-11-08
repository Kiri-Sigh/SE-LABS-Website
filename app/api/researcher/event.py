from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
import json
from pydantic import ValidationError

from ...auth import get_current_active_authorized_user
from ...schemas.auth_user import AuthUser
from ...schemas.event_io import EventCreate
from ...schemas.event_thumbnail import EventThumbnail, ET01
from ...crud.event import create_event
from ...dependencies import get_db

router = APIRouter(
    prefix="/researcher/event",
    tags=["event"],
)

@router.post("/", response_model=EventThumbnail)
async def create_events_API(
    research_id: Optional[UUID] = Query(None),
    laboratory_id: Optional[UUID] = Query(None),
    event: str = Form(...),
    image: UploadFile = File(...),
    current_user: AuthUser = Depends(get_current_active_authorized_user),
    db: Session = Depends(get_db)
):  
    """
    event must come in this form \n
    {
        "title": str,
        "body": str,
        "location": str,
        "start": "2023-04-15T10:00:00",
        "end": "2023-04-15T12:00:00",
        "related_laboratory": {
            "LID": UUID,
            "related_research": {
                "RID": UUID
            }
        }
    }
    """

    if image.content_type not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG images are allowed")
    
    event_data = None
    event_object: EventCreate = None
    
    try:
        event_data = json.loads(event)
        event_object = EventCreate.model_validate(event_data)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON in event field: " + str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")
    
    new_event = await create_event(
        event=event_object,
        image=image,
        research_id=research_id,
        laboratory_id=laboratory_id,
        db=db
    )

    return ET01.to_event_thumbnail(new_event)