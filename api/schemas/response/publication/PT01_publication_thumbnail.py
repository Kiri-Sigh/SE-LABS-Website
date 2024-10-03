from pydantic import BaseModel

class PT01(BaseModel):
    pid: str
    title: str
    body: str
    link: str