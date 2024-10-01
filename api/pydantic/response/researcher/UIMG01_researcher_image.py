from pydantic import BaseModel

class NIMG01(BaseModel):
    uid: str
    image: bytes