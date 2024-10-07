import base64
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ...dependency.database import get_db
from ...schemas.response.event.RET01_response_event_thumbnail import RET01
from ...schemas.response.event.ET01_event_thumbnail import ET01
from ...schemas.response.event.EIMGH01_event_image_high import EIMGH01
from ...schemas.response.event.EIMGL01_event_image_low import EIMGL01
from ...schemas.util.ImageResponse import ImageResponse
from ...models import model as models
from ...schemas.util.image import ImageInterface

router = APIRouter(
    prefix="/user/event",
    tags=["event"],
)

@router.get("/thumbnail", response_model=List[RET01])
async def get_event_thumbnail(
    laboratory_id: Optional[UUID] = Query(None, description="Filter by laboratory ID"),
    research_id: Optional[UUID] = Query(None, description="Filter by research ID"),
    amount: int = Query(10, ge=1, le=100, description="Number of events to return"),
    page: int = Query(1, ge=1, description="Page number"),
    db: AsyncSession = Depends(get_db)
) -> List[RET01]:
    """
    Retrieve event thumbnails with optional filtering and pagination.

    Args:
        laboratory_id (Optional[UUID]): Filter events by laboratory ID.
        research_id (Optional[UUID]): Filter events by research ID.
        amount (int): Number of events to return per page (1-100).
        page (int): Page number for pagination.
        db (Session): Database session.

    Returns:
        List[RET01]: List of event thumbnails.
    """
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
    db: AsyncSession = Depends(get_db)
) -> ImageResponse:
    """
    Retrieve high-resolution image for a specific event.

    Args:
        event_id (UUID): The ID of the event.
        db (Session): Database session.

    Returns:
        ImageResponse: High-resolution image data.

    Raises:
        HTTPException: If the event or image is not found.
    """
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if not event.image_high:
        raise HTTPException(status_code=404, detail="High resolution image not found for this event")
    
    image_data = ImageInterface._ensure_jpg(event.image_high)
    return ImageResponse(
        image=EIMGH01(eid=event.event_id, image=base64.b64encode(image_data).decode('utf-8'))
    )

@router.get("/image-low", response_model=ImageResponse)
async def get_event_image_low(
    event_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> ImageResponse:
    """
    Retrieve low-resolution image for a specific event.

    Args:
        event_id (UUID): The ID of the event.
        db (Session): Database session.

    Returns:
        ImageResponse: Low-resolution image data.

    Raises:
        HTTPException: If the event or image is not found.
    """
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if not event.image_low:
        raise HTTPException(status_code=404, detail="Low resolution image not found for this event")
    
    image_data = ImageInterface._ensure_jpg(event.image_low)
    return ImageResponse(
        image=EIMGL01(eid=str(event.event_id), image=base64.b64encode(image_data).decode('utf-8'))
    )