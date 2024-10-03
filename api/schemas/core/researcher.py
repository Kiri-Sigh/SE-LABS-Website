from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from abc import ABC

from ..util.image import ImageInterface

class ResearcherInterface(BaseModel, ImageInterface, ABC):
    full_name: str
    gmail: EmailStr

    def __new__(cls, *args, **kwargs):
        if cls is ResearcherInterface:
            raise TypeError(f"{cls.__name__} is an abstract class and cannot be instantiated directly.")
        return super().__new__(cls)
    
class ResearcherCreate(ResearcherInterface):
    pass

class ResearcherDB(ResearcherInterface):
    user_id: UUID
    highest_role: str
    admin: bool
    labs: list[UUID]
    researches: list[UUID]

    model_config = ConfigDict(from_attributes=True)