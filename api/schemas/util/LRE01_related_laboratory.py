from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from api.schemas.util.RRE01_related_research import RRE01
from api.schemas.response.publication.unreadable.PRE01_publication_related import PRE01

class LRE01(BaseModel):
    lid: UUID
    title: str
    related_research: Optional[RRE01] = None
    related_publication: Optional[PRE01] = None