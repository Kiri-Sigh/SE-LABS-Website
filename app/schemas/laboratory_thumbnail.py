from pydantic import BaseModel
from uuid import UUID

class LT01(BaseModel):
    LID: UUID
    title: str
    body: str

class LaboratoryThumbnail(BaseModel):
    Laboratory: LT01