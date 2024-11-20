from pydantic import BaseModel, HttpUrl, ConfigDict
from uuid import UUID

from .ult.LRE02 import LRE02

class PT01(BaseModel):
    PID: UUID
    title: str
    body: str
    link: HttpUrl
    related_laboratory: LRE02

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            PID=obj.publication_id,
            title=obj.publication_name,
            body=obj.body,
            link=obj.url,
            related_laboratory=cls._get_related_laboratory(obj)
        )
    
    @staticmethod
    def _get_related_laboratory(obj) -> LRE02:
        if obj.lab:
            return LRE02.from_orm(obj.lab)
        return None
    
    @classmethod
    def to_publication_thumbnail(cls, event) -> 'PublicationThumbnail':
        et01 = cls.from_orm(event)
        return PublicationThumbnail(Publication=et01)

class PublicationThumbnail(BaseModel):
    Publication: PT01

    model_config = ConfigDict(from_attributes=True)