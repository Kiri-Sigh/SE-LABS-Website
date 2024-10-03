from pydantic import BaseModel

class LIMG01(BaseModel):
    lid: str
    image: bytes