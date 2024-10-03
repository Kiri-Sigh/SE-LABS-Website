from pydantic import BaseModel
from uuid import UUID

class LU01(BaseModel):
    lid: UUID
    title: str
    body: str
    image: bytes