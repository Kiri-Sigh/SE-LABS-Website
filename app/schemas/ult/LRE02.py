from pydantic import BaseModel, ConfigDict
from uuid import UUID

class LRE02(BaseModel):
    LID: UUID
    title: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            LID=obj.lab_id,
            title=obj.lab_name
        )