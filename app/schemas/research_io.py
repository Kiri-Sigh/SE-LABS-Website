from uuid import UUID
from pydantic import BaseModel, model_validator, ConfigDict
from typing import Optional
from datetime import datetime

from .ult.LRE04 import LRE04

class ResearchCreate(BaseModel):
    title: str
    body: str
    related_laboratory: LRE04

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm(obj):
        return ResearchCreate(
            title=obj.title,
            body=obj.body,
            related_laboratory=LRE04.from_orm(obj)
        )
    
class ResearchUpdate(BaseModel):
    RID: UUID
    title: str
    body: str
    related_laboratory: LRE04

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm(obj):
        return ResearchUpdate(
            RID=obj.RID,
            title=obj.title,
            body=obj.body,
            related_laboratory=LRE04.from_orm(obj)
        )