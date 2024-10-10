from pydantic import BaseModel
from uuid import UUID
from typing import Optional

from .RRE01 import RRE01
from .PRE01 import PRE01

class LRE01(BaseModel):
    lid: UUID
    title: str
    related_research: Optional[RRE01] = None
    related_publication: Optional[PRE01] = None