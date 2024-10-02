from pydantic import BaseModel

from api.pydantic.response.laboratory.LRE02_related_laboratory import LRE02

class RT01(BaseModel):
    rid: str
    title: str
    body: str
    related_laboratory: LRE02