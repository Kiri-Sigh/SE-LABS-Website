from pydantic import BaseModel
from uuid import UUID

from ...util.image import ImageInterface

class EIMGH01(BaseModel):
    eid: UUID
    image: bytes

    @classmethod
    def from_orm(cls, obj):
        return cls(
            eid=str(obj.event_id),
            image=ImageInterface._ensure_jpg(obj.image_high)
        )