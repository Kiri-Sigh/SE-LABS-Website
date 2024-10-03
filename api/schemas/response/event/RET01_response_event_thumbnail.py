from pydantic import BaseModel

from .ET01_event_thumbnail import ET01

class RET01(BaseModel):
    Event: ET01