from pydantic import BaseModel

from ....util import LRE04_related_laboratory as util

class REC01(BaseModel):
    title: str
    body: str
    image: bytes
    relates_laboratory: util.LRE04