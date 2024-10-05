from pydantic import BaseModel, model_validator, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum

from ...util.LRE01_related_laboratory import LRE01
from ...util.RRE01_related_research import RRE01
from ...response.publication.unreadable.PRE01_publication_related import PRE01

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

    # Configure the model to use attributes from ORM
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj):
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
            related_research = None
            related_publication = None
            if obj.publication:
                related_publication = PRE01(
                    pid=obj.publication.publication_id,
                    title=obj.publication.publication_name
                )
                return LRE01(
                    lid=obj.lab.lab_id,
                    title=obj.lab.lab_name,
                    related_publication=related_publication
                )
            elif obj.research:
                related_research = RRE01(
                    rid=obj.research.research_id,
                    title=obj.research.research_name
                )
                return LRE01(
                    lid=obj.lab.lab_id,
                    title=obj.lab.lab_name,
                    related_research=related_research
                )
        return None

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start >= self.end:
            raise ValueError("End time must be after start time")
        return self
