from uuid import UUID
from pydantic import BaseModel, model_validator, ConfigDict
from typing import Optional
from datetime import datetime

from .ult.LRE03 import LRE03

class EventCreate(BaseModel):
    title: str
    body: str
    location: str
    start: datetime
    end: datetime
    related_laboratory: LRE03

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm(obj, related_laboratory = None):
        if related_laboratory is None:
            return EventCreate(
                title=obj.title,
                body=obj.body,
                location=obj.location,
                start=obj.start,
                end=obj.end,
                related_laboratory=None
            )
        else:
            return EventCreate(
                title=obj.title,
                body=obj.body,
                location=obj.location,
                start=obj.start,
                end=obj.end,
                related_laboratory=LRE03.from_orm(obj.related_laboratory)
            )

class EventDB(BaseModel):
    event_id: UUID
    title: str
    body: str
    location: str
    start: datetime
    end: datetime
    posted: bool
    related_laboratory: LRE03

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm(obj, related_laboratory = None):
        if related_laboratory is None:
            return EventDB(
                news_id=obj.event_id,
                title=obj.event_name,
                body=obj.body,
                location=obj.location,
                start=obj.date_start,
                end=obj.date_end,
                posted=obj.posted,
                related_laboratory=None
            )
        else:
            return EventDB(
                news_id=obj.event_id,
                title=obj.event_name,
                body=obj.body,
                location=obj.location,
                start=obj.date_start,
                end=obj.date_end,
                posted=obj.posted,
                related_laboratory=LRE03.from_orm(obj.related_laboratory)
            )