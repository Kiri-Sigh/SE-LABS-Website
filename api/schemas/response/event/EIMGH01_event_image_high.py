from pydantic import BaseModel

class EIMGH01(BaseModel):
    eid: str
    image: bytes

    @classmethod
    def from_orm(cls, obj):
        return cls(
            eid=str(obj.event_id),
            image=obj.image_high
        )