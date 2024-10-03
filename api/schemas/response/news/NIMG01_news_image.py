from pydantic import BaseModel

class NIMG01(BaseModel):
    nid: str
    image: bytes