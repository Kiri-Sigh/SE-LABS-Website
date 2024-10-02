from pydantic import BaseModel

class UIMG01(BaseModel):
    uid: str
    image: bytes