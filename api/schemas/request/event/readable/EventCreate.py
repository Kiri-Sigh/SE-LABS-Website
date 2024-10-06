from pydantic import BaseModel

from ..unreadable import EC01_event_create as unreadable

class EventCreate(BaseModel):
    Event: unreadable.EC01