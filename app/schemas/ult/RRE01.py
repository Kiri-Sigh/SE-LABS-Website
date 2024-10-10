from pydantic import BaseModel
from uuid import UUID

class RRE01(BaseModel):
    rid: UUID
    title: str