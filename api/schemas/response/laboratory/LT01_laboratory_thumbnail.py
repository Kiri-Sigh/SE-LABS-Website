from pydantic import BaseModel

class LT01(BaseModel):
    lid: str
    title: str
    body: str