from pydantic import BaseModel
from uuid import UUID

class PRE01(BaseModel):
    pid: UUID
    title: str