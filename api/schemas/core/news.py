from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from abc import ABC

from ..util.image import ImageInterface

class NewsInterface(BaseModel, ImageInterface, ABC):
    news_name: str
    body: str
    lab_id: Optional[UUID] = None
    research_id: Optional[UUID] = None
    publication_id: Optional[UUID] = None

    def __new__(cls, *args, **kwargs):
        if cls is NewsInterface:
            raise TypeError(f"{cls.__name__} is an abstract class and cannot be instantiated directly.")
        return super().__new__(cls)

class NewsCreate(NewsInterface):
    pass

class NewsDB(NewsInterface):
    news_id : UUID
    date: datetime

    model_config = ConfigDict(from_attributes=True)