from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

from model import Laboratory, Research, Publication
from .RRE01 import RRE01
from .PRE01 import PRE01

class LRE01(BaseModel):
    LID: UUID
    title: str
    related_research: Optional[RRE01] = None
    related_publication: Optional[PRE01] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, lab: Laboratory, research_id: Optional[UUID] = None, publication_id: Optional[UUID] = None) -> 'LRE01':
        research: Research = None
        publication: Publication = None

        for r in lab.researches:
            if r.research_id == research_id:
                research = r
                break

        for p in lab.publications:
            if p.publication_id == publication_id:
                publication = p
                break

        return cls(
            LID=lab.lab_id,
            title=lab.lab_name,
            related_research=RRE01.from_orm(research) if research_id else None,
            related_publication=PRE01.from_orm(publication) if publication_id else None
        )