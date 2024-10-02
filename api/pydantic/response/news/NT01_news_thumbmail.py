from pydantic import BaseModel
from typing import Optional

from api.pydantic.response.laboratory.LRE01_related_laboratory import LRE01

class NT01(BaseModel):
    nid: str
    title: str
    body: str
    date: str
    related_laboratory: Optional[LRE01] = None