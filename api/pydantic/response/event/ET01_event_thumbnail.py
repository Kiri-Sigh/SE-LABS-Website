from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

from api.pydantic.response.laboratory.LRE01_related_laboratory import LRE01

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

    @classmethod
    def model_validate(cls, obj):
        if isinstance(obj.get('EID'), str):
            obj['EID'] = UUID(obj['EID'])
        for field in ['start', 'end']:
            if isinstance(obj.get(field), str):
                obj[field] = datetime.fromisoformat(obj[field])
        return super().model_validate(obj)

    @field_validator('status', mode='before')
    def set_status(cls, v, info):
        now = datetime.now()
        start = info.data.get('start')
        end = info.data.get('end')

        if not start or not end:
            raise ValueError("Start and end times must be provided")

        if now < start:
            return EventStatus.COMING
        elif start <= now <= end:
            return EventStatus.ON_GOING
        else:
            return EventStatus.FINISHED

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start >= self.end:
            raise ValueError("End time must be after start time")
        return self

    @classmethod
    def from_orm(cls, obj):
        return cls.model_validate(obj.__dict__)