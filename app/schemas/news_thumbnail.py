from uuid import UUID
from pydantic import BaseModel, model_validator, ConfigDict
from typing import Optional
from datetime import datetime

from .ult.LRE01 import LRE01

class NT01(BaseModel):
    NID: UUID
    title: str
    body: str
    date: datetime
    related_laboratory: Optional[LRE01] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            NID=obj.news_id,
            title=obj.news_name,
            body=obj.body,
            date=obj.date,
            related_laboratory=cls._get_related_laboratory(obj)
        )
    
    @staticmethod
    def _get_related_laboratory(obj) -> Optional[LRE01]:
        if obj.lab:
            if obj.research_id:
                return LRE01.from_orm(obj.lab, obj.research_id)
            return LRE01.from_orm(obj.lab)
        return None
    
    @classmethod
    def to_news_thumbnail(cls, event) -> 'NewsThumbnail':
        nt01 = cls.from_orm(event)
        return NewsThumbnail(News=nt01)

class NewsThumbnail(BaseModel):
    News: NT01

    model_config = ConfigDict(from_attributes=True)