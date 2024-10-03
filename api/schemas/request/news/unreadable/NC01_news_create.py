from pydantic import BaseModel

from ....util import LRE03_related_laboratory as util

class NC01(BaseModel):
    title: str
    body: str
    image: bytes
    related_laboratory: util.LRE03