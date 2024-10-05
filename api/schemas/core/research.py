from pydantic import BaseModel, ConfigDict
from uuid import UUID

from ..util.image import ImageInterface

class ResearchInterface(BaseModel, ImageInterface):
    research_name: str
    body: str
    lab_id: UUID

    
class ResearchCreate(ResearchInterface):
    pass

class ResearchDB(ResearchInterface):
    research_id: UUID
    news: list[UUID]
    events: list[UUID]

    model_config = ConfigDict(from_attributes=True)