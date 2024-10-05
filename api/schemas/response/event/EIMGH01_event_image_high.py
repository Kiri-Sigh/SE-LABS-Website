from pydantic import BaseModel

from ...util.image import ImageInterface

class EIMGH01(BaseModel):
    eid: str
    image: bytes

    @classmethod
    def from_orm(cls, obj):
        return cls(
            eid=str(obj.event_id),
            image=ImageInterface._ensure_jpg(obj.image_high)
        )