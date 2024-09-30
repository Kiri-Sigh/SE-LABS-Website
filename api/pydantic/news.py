from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

from .image import ImageInterface

class NewsBase(BaseModel):
    news_name: str
    body: str
    date: datetime
    posted: bool
    lab_id: Optional[str] = None
    project_id: Optional[str] = None
    publication_id: Optional[str] = None

class NewsCreate(NewsBase, ImageInterface):
    pass

class NewsDB(NewsBase):
    news_id: UUID
    image_high: bytes
    image_low: bytes

    model_config = ConfigDict(from_attributes=True)
