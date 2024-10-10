from pydantic import BaseModel
from uuid import UUID

class LRE02(BaseModel):
    lid: UUID
    title: str