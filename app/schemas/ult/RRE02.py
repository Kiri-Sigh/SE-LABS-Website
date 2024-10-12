from pydantic import BaseModel, ConfigDict
from uuid import UUID

class RRE02(BaseModel):
    RID: UUID

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            RID=obj.research_id,
        )