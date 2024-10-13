from pydantic import BaseModel, model_validator, ConfigDict
from uuid import UUID

class LT01(BaseModel):
    LID: UUID
    title: str
    body: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            LID=obj.lab_id,
            title=obj.lab_name,
            body=obj.body
        )
    
    @classmethod
    def to_laboratory_thumbnail(cls, lab) -> 'LaboratoryThumbnail':
        ltb = cls.from_orm(lab)
        return LaboratoryThumbnail(Laboratory=ltb)

class LaboratoryThumbnail(BaseModel):
    Laboratory: LT01

    model_config = ConfigDict(from_attributes=True)