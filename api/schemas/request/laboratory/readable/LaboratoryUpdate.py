from pydantic import BaseModel

# from ..unreadable import LC01_laboratory_create as unreadable
from ..unreadable import LU01_laboratory_update as unreadable

class LaboratoryUpdate(BaseModel):
    Laboratory: unreadable.LU01