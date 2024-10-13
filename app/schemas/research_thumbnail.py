from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional

from .ult.LRE02 import LRE02

class RT01(BaseModel):
    RID: UUID
    title: str
    body: str
    related_laboratory: LRE02

    model_config = ConfigDict(from_attributes=True)
    
    @classmethod
    def from_orm(cls, obj):
        return cls(
            RID=obj.research_id,
            title=obj.research_name,
            body=obj.body,
            related_laboratory=cls._get_related_laboratory(obj)
        )
    
    @staticmethod
    def _get_related_laboratory(obj) -> Optional[LRE02]:
        if obj.lab:
            return LRE02.from_orm(obj.lab)
        return None
    
    @classmethod
    def to_research_thumbnail(cls, event) -> 'ResearchThumbnail':
        rt01 = cls.from_orm(event)
        return ResearchThumbnail(Research=rt01)

class ResearchThumbnail(BaseModel):
    Research: RT01

    model_config = ConfigDict(from_attributes=True)