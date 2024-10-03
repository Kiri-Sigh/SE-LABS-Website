from pydantic import BaseModel

class REU01(BaseModel):
    rid: str
    title: str
    body: str
    image: bytes