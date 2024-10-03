from pydantic import BaseModel, HttpUrl, ConfigDict
from uuid import UUID
from abc import ABC

from ..util.image import ImageInterface

class PublicationInterface(BaseModel, ImageInterface, ABC):
    publication_name: str
    body: str
    publication_link: HttpUrl
    lab_id: UUID

    def __new__(cls, *args, **kwargs):
        if cls is PublicationInterface:
            raise TypeError(f"{cls.__name__} is an abstract class and cannot be instantiated directly.")
        return super().__new__(cls)
    
class PublicationCreate(PublicationInterface):
    pass

class PublicationDB(PublicationInterface):
    publication_id: UUID
    news: list[UUID]
    events: list[UUID]

    model_config = ConfigDict(from_attributes=True)