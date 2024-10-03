from pydantic import BaseModel

class PIMG01(BaseModel):
    pid: str
    image: str