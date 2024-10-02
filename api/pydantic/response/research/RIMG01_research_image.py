from pydantic import BaseModel

class RIMG01(BaseModel):
    rid: str
    image: bytes