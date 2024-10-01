from pydantic import BaseModel
from typing import Optional

class NT01(BaseModel):
    nid: str
    title: str
    body: str
    date: str
    related_laboratory: Optional[REL01] = None