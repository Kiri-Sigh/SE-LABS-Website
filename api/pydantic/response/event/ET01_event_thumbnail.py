from pydantic import BaseModel
from typing import Optional

class ET01(BaseModel):
    EID: str
    title: str
    body: str
    location: str
    start: str
    end: str
    status: str
    related_laboratory: Optional[REL01] = None