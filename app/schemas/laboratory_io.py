from uuid import UUID
from pydantic import BaseModel, model_validator, ConfigDict, HttpUrl
from typing import Optional
from datetime import datetime

class LaboratoryUpdate(BaseModel):
    LID: UUID
    title: Optional[str]
    body: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm(obj):
        return LaboratoryUpdate(
            lab_id=obj.LID,
            title=obj.title,
            body=obj.body
        )

class LaboratoryCreate(BaseModel):
    title: str
    body: str

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm(obj):
        return LaboratoryCreate(
            title=obj.title,
            body=obj.body
        )