from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Optional
from uuid import UUID

from .image import ImageInterface

class PublicationBase(BaseModel):
    publication_name: str
    body: str
    publication_link: HttpUrl
    lab_id: str

class PublicationCreate(PublicationBase, ImageInterface):
    pass

class PublicationDB(PublicationBase):
    publication_id: UUID
    image_high: bytes
    image_low: bytes

    model_config = ConfigDict(from_attributes=True)