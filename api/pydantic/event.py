from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

from .image import ImageInterface

class EventsBase(BaseModel):
    event_name: str
    body: str
    location: str
    date_start: datetime
    date_end: datetime
    posted: bool
    lab_id: Optional[str] = None
    project_id: Optional[str] = None
    publication_id: Optional[str] = None

class EventsCreate(EventsBase, ImageInterface):
    pass

class EventsDB(EventsBase):
    event_id: UUID
    image_high: bytes
    image_low: bytes

    model_config = ConfigDict(from_attributes=True)