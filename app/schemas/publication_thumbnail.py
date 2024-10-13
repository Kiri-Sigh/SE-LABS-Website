from pydantic import BaseModel, HttpUrl, ConfigDict
from uuid import UUID

class PT01(BaseModel):
    PID: UUID
    title: str
    body: str
    link: HttpUrl

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        return cls(
            PID=obj.publication_id,
            title=obj.publication_name,
            body=obj.body,
            link=obj.url
        )
    
    @classmethod
    def to_publication_thumbnail(cls, event) -> 'PublicationThumbnail':
        et01 = cls.from_orm(event)
        return PublicationThumbnail(Publication=et01)

class PublicationThumbnail(BaseModel):
    Publication: PT01

    model_config = ConfigDict(from_attributes=True)