from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from ...dependency.database import get_db
from ...pydantic.response.event.ET01_event_thumbnail import ET01
from ...pydantic.response.event.EIMG01_event_image import EIMG01

router = APIRouter(
    prefix="/user/event",
    tags=["event"],
)

@router.get("/thumbnail", response_model=list[ET01])
async def get_event_thumbnail(
        laboratory_id: Optional[str] = None,
        research_id: Optional[str] = None,
        amount: Optional[int] = 0,
        page: Optional[int] = 0,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get event thumbnail"}

@router.get("/image-high", response_model=EIMG01)
async def get_event_image_high(
        event_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get event image high"}

@router.get("/image-low", response_model=EIMG01)
async def get_event_image_low(
        event_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get event image low"}