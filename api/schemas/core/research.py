from pydantic import BaseModel, ConfigDict
from uuid import UUID
from abc import ABC

from ..util.image import ImageInterface

class ResearchInterface(BaseModel, ImageInterface, ABC):
    research_name: str
    body: str
    lab_id: UUID

    def __new__(cls, *args, **kwargs):
        if cls is ResearchInterface:
            raise TypeError(f"{cls.__name__} is an abstract class and cannot be instantiated directly.")
        return super().__new__(cls)
    
class ResearchCreate(ResearchInterface):
    pass

class ResearchDB(ResearchInterface):
    research_id: UUID
    news: list[UUID]
    events: list[UUID]

    model_config = ConfigDict(from_attributes=True)