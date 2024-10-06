from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

from ..util.image import ImageInterface

class EventInterface(ImageInterface):
    event_name: str
    body: str
    location: str
    date_start: datetime
    date_end: datetime
    lab_id: Optional[UUID] = None
    research_id: Optional[UUID] = None
    publication_id: Optional[UUID] = None
    
class EventCreate(EventInterface):
    pass

class EventDB(EventInterface):
    event_id: UUID

    model_config = ConfigDict(from_attributes=True)