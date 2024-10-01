from pydantic import BaseModel

class NIMG01(BaseModel):
    rid: str
    image: bytes