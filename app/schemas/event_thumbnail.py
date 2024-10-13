from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, model_validator, ConfigDict
from uuid import UUID

from .ult.LRE01 import LRE01

class EventStatus(str, Enum):
    COMING = "Coming"
    ON_GOING = "On Going"
    FINISHED = "Finished"

class ET01(BaseModel):
    EID: UUID
    title: str
    body: str
    location: str
    start: datetime
    end: datetime
    status: EventStatus
    related_laboratory: Optional[LRE01] = None

    model_config = ConfigDict(from_attributes=True)

    # Convert SQLAlchemy model fields to ET01 model fields
    @classmethod
    def from_orm(cls, obj):
        return cls(
            EID=obj.event_id,
            title=obj.event_name,
            body=obj.body,
            location=obj.location,
            start=obj.date_start,
            end=obj.date_end,
            status=cls._determine_status(obj.date_start, obj.date_end),
            related_laboratory=cls._get_related_laboratory(obj)
        )

    @staticmethod
    def _determine_status(start: datetime, end: datetime) -> EventStatus:
        now = datetime.now()
        if now < start:
            return EventStatus.COMING
        elif start <= now <= end:
            return EventStatus.ON_GOING
        else:
            return EventStatus.FINISHED
        
    @staticmethod
    def _get_related_laboratory(obj) -> Optional[LRE01]:
        if obj.lab:
            return LRE01.from_orm(obj.lab)
        return None

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start >= self.end:
            raise ValueError("End time must be after start time")
        return self
    
    @classmethod
    def to_event_thumbnail(cls, event) -> 'EventThumbnail':
        et01 = cls.from_orm(event)
        return EventThumbnail(Event=et01)

class EventThumbnail(BaseModel):
    Event: ET01
    
    model_config = ConfigDict(from_attributes=True)