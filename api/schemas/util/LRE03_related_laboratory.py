from pydantic import BaseModel

from .RRE02_related_research import RRE02

class LRE03(BaseModel):
    lid: str
    related_research: RRE02