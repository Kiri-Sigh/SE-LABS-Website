from pydantic import BaseModel

from ....util import LRE04_related_laboratory, RRE02_related_research

class RC01(BaseModel):
    name: str
    mail: str
    password: str
    image: bytes
    related_research: RRE02_related_research.RRE02
    related_laboratory: LRE04_related_laboratory.LRE04