from pydantic import BaseModel, ConfigDict
from uuid import UUID

from .image import ImageInterface

class LabBase(BaseModel):
    lab_name: str
    body: str

class LabCreate(LabBase, ImageInterface):
    pass

class LabDB(LabBase):
    lab_id: UUID
    image_high: bytes
    image_low: bytes

    model_config = ConfigDict(from_attributes=True)