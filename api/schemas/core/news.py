from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

from ..util.image import ImageInterface

class NewsInterface(BaseModel, ImageInterface):
    news_name: str
    body: str
    lab_id: Optional[UUID] = None
    research_id: Optional[UUID] = None
    publication_id: Optional[UUID] = None

class NewsCreate(NewsInterface):
    pass

class NewsDB(NewsInterface):
    news_id : UUID
    date: datetime

    model_config = ConfigDict(from_attributes=True)