from pydantic import BaseModel

from ..unreadable import EC01_event_create as unreadable

class EventCreate(BaseModel):
    News: unreadable.EC01