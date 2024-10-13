from pydantic import BaseModel, ConfigDict
from uuid import UUID

from .RRE02 import RRE02

class LRE03(BaseModel):
    LID: UUID
    related_research: RRE02

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj, related_research = None):
        if related_research is None:
            return cls(
                LID=obj.lab_id,
                related_research=None
            )
        else:
            return cls(
                LID=obj.lab_id,
                related_research=RRE02.from_orm(obj.related_research)
            )