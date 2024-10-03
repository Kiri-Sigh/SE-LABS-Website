from pydantic import BaseModel, HttpUrl

class PT01(BaseModel):
    link: HttpUrl