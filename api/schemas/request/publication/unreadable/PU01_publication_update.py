from pydantic import BaseModel, HttpUrl

class PU01(BaseModel):
    pid: str
    title: str
    body: str
    link: HttpUrl
    image: bytes