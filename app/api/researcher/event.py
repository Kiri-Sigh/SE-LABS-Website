from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from uuid import UUID, uuid4
from datetime import datetime
import json
from pydantic import ValidationError

from ...dependencies import get_db, process_image
from ...auth import get_current_active_researcher
from ...model import *
from ...schemas.auth_user import AuthUser
from ...schemas.event_io import EventCreate
from ...schemas.event_thumbnail import EventThumbnail, ET01

router = APIRouter(
    prefix="/researcher/event",
    tags=["event"],
)

@router.post("/", response_model=EventThumbnail)
async def create_event(
    research_id: UUID,
    event: str = Form(...),
    image: UploadFile = File(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_researcher)
):
    if image.content_type not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG images are allowed")
    
    try:
        # Manually parse the JSON string
        event_data = json.loads(event)
        # Validate the parsed data against your Pydantic model
        event_object = EventCreate.model_validate(event_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in event field")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    processed_images = await process_image(image)
    high_res, low_res = processed_images
    
    new_event = Event(
        event_id=uuid4(),
        event_name=event_object.title,
        image_high=high_res,
        image_low=low_res,
        body=event_object.body,
        location=event_object.location,
        date_start=event_object.start,
        date_end=event_object.end,
        posted=False,
        lab_id=event_object.related_laboratory.LID,
        research_id=research_id
    )
    
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return ET01.to_event_thumbnail(new_event)