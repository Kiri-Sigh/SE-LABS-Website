from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from .ult.LRE01 import LRE01

class NT01(BaseModel):
    nid: UUID
    title: str
    body: str
    date: datetime
    related_laboratory: LRE01

class NewsThumbnail(BaseModel):
    News: NT01