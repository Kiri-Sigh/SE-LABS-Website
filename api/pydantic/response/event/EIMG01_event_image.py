from pydantic import BaseModel

class EIMG01(BaseModel):
    eid: str
    image: bytes