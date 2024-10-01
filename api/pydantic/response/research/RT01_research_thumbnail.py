from pydantic import BaseModel

class RT01(BaseModel):
    rid: str
    title: str
    body: str
    related_laboratory: REL02