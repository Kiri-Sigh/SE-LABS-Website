from pydantic import BaseModel, HttpUrl, ConfigDict
from uuid import UUID

from ..util.image import ImageInterface

class PublicationInterface(BaseModel, ImageInterface):
    publication_name: str
    body: str
    publication_link: HttpUrl
    lab_id: UUID
    
class PublicationCreate(PublicationInterface):
    pass

class PublicationDB(PublicationInterface):
    publication_id: UUID
    news: list[UUID]
    events: list[UUID]

    model_config = ConfigDict(from_attributes=True)