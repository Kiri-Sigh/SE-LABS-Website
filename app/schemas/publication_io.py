from uuid import UUID
from pydantic import BaseModel, model_validator, ConfigDict, HttpUrl
from typing import Optional
from datetime import datetime

class PublicationUpdate(BaseModel):
    PID: UUID
    title: Optional[str]
    body: Optional[str]
    link: Optional[HttpUrl]

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm(obj):
        return PublicationUpdate(
            PID=obj.PID,
            title=obj.title,
            body=obj.body,
            link=obj.link
        )
    