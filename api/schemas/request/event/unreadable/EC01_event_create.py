from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from ....util import LRE03_related_laboratory as util

class EC01(BaseModel):
    title: str
    body: str
    location: str
    date_start: datetime
    date_end: datetime
    image_high: bytes
    related_laboratory: Optional[util.LRE03] = None