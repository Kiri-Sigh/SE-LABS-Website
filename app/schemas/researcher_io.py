from uuid import UUID
from pydantic import BaseModel, model_validator, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

class ResearcherCreate(BaseModel):
    password: str
    name: str
    mail: EmailStr
    
    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm(obj):
        return ResearcherCreate(
            password=obj.password,
            name=obj.name,
            mail=obj.mail
        )