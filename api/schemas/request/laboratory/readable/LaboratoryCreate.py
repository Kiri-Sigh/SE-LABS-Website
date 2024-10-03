from pydantic import BaseModel

from ..unreadable import LC01_laboratory_create as unreadable

class LaboratoryCreate(BaseModel):
    Laboratory: unreadable.LC01