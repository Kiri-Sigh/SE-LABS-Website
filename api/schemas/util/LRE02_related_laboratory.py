from pydantic import BaseModel

class LRE02(BaseModel):
    lid: str
    title: str