from uuid import UUID
from pydantic import BaseModel

from .ult.LRE02 import LRE02

class RT01(BaseModel):
    rid: UUID
    title: str
    body: str
    related_laboratory: LRE02

class ResearchThumbnail(BaseModel):
    Research: RT01