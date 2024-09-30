from pydantic import BaseModel, ConfigDict
from uuid import UUID

from .image import ImageInterface

class ProjectBase(BaseModel):
    project_name: str
    body: str
    lab_id: str

class ProjectCreate(ProjectBase, ImageInterface):
    pass

class ProjectDB(ProjectBase):
    project_id: UUID
    image_high: bytes
    image_low: bytes

    model_config = ConfigDict(from_attributes=True)