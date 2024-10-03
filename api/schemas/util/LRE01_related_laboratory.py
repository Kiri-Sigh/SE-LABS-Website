from pydantic import BaseModel

from api.schemas.util.RRE01_related_research import RRE01

class LRE01(BaseModel):
    lid: str
    title: str
    related_research: RRE01