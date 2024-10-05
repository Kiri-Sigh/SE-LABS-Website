from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

from ..util.image import ImageInterface

class ResearcherInterface(BaseModel, ImageInterface):
    full_name: str
    gmail: EmailStr
    
class ResearcherCreate(ResearcherInterface):
    pass

class ResearcherDB(ResearcherInterface):
    user_id: UUID
    highest_role: str
    admin: bool
    labs: list[UUID]
    researches: list[UUID]

    model_config = ConfigDict(from_attributes=True)