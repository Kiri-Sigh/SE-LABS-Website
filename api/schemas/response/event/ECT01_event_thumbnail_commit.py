from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

from api.schemas.response.laboratory.ult.LRE01_related_laboratory import LRE01

class EventStatus(str, Enum):
    COMING = "Coming"
    ON_GOING = "On Going"
    FINISHED = "Finished"

class ECT01(BaseModel):
    EID: UUID
    title: str
    body: str
    location: str
    start: datetime
    end: datetime
    related_laboratory: Optional[LRE01] = None

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
        if obj.laboratory:
            return LRE01.from_orm(obj.laboratory)
        return None

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start >= self.end:
            raise ValueError("End time must be after start time")
        return self