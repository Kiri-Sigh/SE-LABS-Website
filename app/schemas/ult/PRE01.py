from pydantic import BaseModel, ConfigDict
from uuid import UUID

class PRE01(BaseModel):
    pid: UUID
    title: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            pid=obj.publication_id,
            title=obj.publication_name
        )