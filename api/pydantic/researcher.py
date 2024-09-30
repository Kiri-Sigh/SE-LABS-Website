from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

from .image import ImageInterface

class PeopleBase(BaseModel):
    fullname: str
    gmail: EmailStr
    token: str

class PeopleCreate(PeopleBase, ImageInterface):
    pass

class PeopleDB(PeopleBase):
    user_id: UUID
    image_high: bytes
    image_low: bytes

    model_config = ConfigDict(from_attributes=True)