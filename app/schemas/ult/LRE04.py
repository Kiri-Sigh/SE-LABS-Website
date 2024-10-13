from pydantic import BaseModel, ConfigDict
from uuid import UUID

class LRE04(BaseModel):
    LID: UUID

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            LID=obj.lab_id
        )