from pydantic import BaseModel

class RRE01(BaseModel):
    rid: str
    title: str