from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from abc import ABC

from ..util.image import ImageInterface

class EventsInterface(BaseModel, ImageInterface, ABC):
    event_name: str
    body: str
    location: str
    date_start: datetime
    date_end: datetime
    lab_id: Optional[UUID] = None
    research_id: Optional[UUID] = None
    publication_id: Optional[UUID] = None

    def __new__(cls, *args, **kwargs):
        if cls is EventsInterface:
            raise TypeError(f"{cls.__name__} is an abstract class and cannot be instantiated directly.")
        return super().__new__(cls)
    
class EventsCreate(EventsInterface):
    pass

class EventsDB(EventsInterface):
    event_id: UUID

    model_config = ConfigDict(from_attributes=True)