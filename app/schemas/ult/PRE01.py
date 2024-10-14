from pydantic import BaseModel, ConfigDict
from uuid import UUID

class PRE01(BaseModel):
    PID: UUID
    title: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            PID=obj.publication_id,
            title=obj.publication_name
        )