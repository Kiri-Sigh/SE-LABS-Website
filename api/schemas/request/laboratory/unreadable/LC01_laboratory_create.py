from pydantic import BaseModel

class LC01(BaseModel):
    title: str
    body: str
    image: bytes