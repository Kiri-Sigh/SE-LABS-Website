from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

from .RRE01 import RRE01
from .PRE01 import PRE01

class LRE01(BaseModel):
    LID: UUID
    title: str
    related_research: Optional[RRE01] = None
    related_publication: Optional[PRE01] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            LID=obj.lab_id,
            title=obj.lab_name,
            related_research=RRE01.from_orm(obj.researches[0]) if obj.researches else None,
            related_publication=PRE01.from_orm(obj.publications[0]) if obj.publications else None
        )