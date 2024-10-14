
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

from .ult.LRE02 import LRE02
from .ult.RRE01 import RRE01
from .ult.position import Position

class UT01(BaseModel):
    UID: UUID
    name: str
    gmail: EmailStr
    position: Position
    related_laboratory: list[LRE02]
    related_research: list[RRE01]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            UID=obj.user_id,
            name=obj.full_name,
            gmail=obj.gmail,
            position=obj.highest_role,
            related_laboratory=cls._get_related_laboratory(obj),
            related_research=cls._get_related_research(obj)
        )
    
    @staticmethod
    def _get_related_laboratory(obj) -> list[LRE02]:
        if obj.labs:
            return [LRE02.from_orm(lab) for lab in obj.labs]
        return []
    
    @staticmethod
    def _get_related_research(obj) -> list[RRE01]:
        if obj.researches:
            return [RRE01.from_orm(research) for research in obj.researches]
        return []
    
    @classmethod
    def to_researcher_thumbnail(cls, event) -> 'ResearcherThumbnail':
        ut01 = cls.from_orm(event)
        return ResearcherThumbnail(Researcher=ut01)

class ResearcherThumbnail(BaseModel):
    Researcher: UT01

    model_config = ConfigDict(from_attributes=True)