from pydantic import BaseModel, ConfigDict
from uuid import UUID

from ..util.image import ImageInterface

class LabInterface(BaseModel, ImageInterface): 
    lab_name: str
    body: str

class LabCreate(LabInterface):
    pass

class LabDB(LabInterface):
    lab_id: UUID
    researches: list[UUID]
    publications: list[UUID]
    news: list[UUID]
    events: list[UUID]

    model_config = ConfigDict(from_attributes=True)