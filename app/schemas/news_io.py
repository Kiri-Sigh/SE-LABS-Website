from uuid import UUID
from pydantic import BaseModel, model_validator, ConfigDict
from typing import Optional
from datetime import datetime

from .ult.LRE03 import LRE03

class NewsCreate(BaseModel):
    title: str
    body: str
    related_laboratory: Optional[LRE03]

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm(obj, related_laboratory = None):
        if related_laboratory is None:
            return NewsCreate(
                title=obj.title,
                body=obj.body,
                related_laboratory=None
            )
        else:
            return NewsCreate(
                title=obj.title,
                body=obj.body,
                related_laboratory=LRE03.from_orm(obj.related_laboratory)
            )

class NewsDB(BaseModel):
    news_id: UUID
    title: str
    body: str
    date: datetime
    posted: bool
    related_laboratory: LRE03

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm(obj, related_laboratory = None):
        if related_laboratory is None:
            return NewsDB(
                news_id=obj.news_id,
                title=obj.news_name,
                body=obj.body,
                date=obj.date,
                posted=obj.posted,
                related_laboratory=None
            )
        else:
            return NewsDB(
                news_id=obj.news_id,
                title=obj.news_name,
                body=obj.body,
                date=obj.date,
                posted=obj.posted,
                related_laboratory=LRE03.from_orm(obj.related_laboratory)
            )