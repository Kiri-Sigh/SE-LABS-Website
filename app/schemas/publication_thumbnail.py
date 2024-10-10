from pydantic import BaseModel, HttpUrl
from uuid import UUID

class PT01(BaseModel):
    pid: UUID
    title: str
    body: str
    link: HttpUrl

class PublicationThumbnail(BaseModel):
    Publication: PT01