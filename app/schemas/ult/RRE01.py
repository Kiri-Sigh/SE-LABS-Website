from pydantic import BaseModel, ConfigDict
from uuid import UUID

class RRE01(BaseModel):
    rid: UUID
    title: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            rid=obj.research_id,
            title=obj.research_name
        )