
from pydantic import BaseModel, EmailStr
from uuid import UUID

from .ult.LRE02 import LRE02
from .ult.RRE01 import RRE01
from .ult.position import Position

class UT01(BaseModel):
    uid: UUID
    name: str
    gmail: EmailStr
    position: Position
    related_laboratory: list[LRE02]
    related_research: list[RRE01]

class ResearcherThumbnail(BaseModel):
    Researcher: UT01