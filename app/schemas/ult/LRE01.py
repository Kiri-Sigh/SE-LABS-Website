from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

from ...model import Laboratory, Research
from .RRE01 import RRE01
from .PRE01 import PRE01

class LRE01(BaseModel):
    LID: UUID
    title: str
    related_research: Optional[RRE01] = None
    related_publication: Optional[PRE01] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, lab: Laboratory, research_id: Optional[UUID] = None):
        research: Research = None
        for r in lab.researches:
            if r.research_id == research_id:
                research = r
                break

        return cls(
            LID=lab.lab_id,
            title=lab.lab_name,
            related_research=RRE01.from_orm(research) if research_id else None,
        )