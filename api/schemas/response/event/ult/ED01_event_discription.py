from pydantic import BaseModel, model_validator, ConfigDict

class ED01(BaseModel):
    eid: str
    description: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj, description: str):
        return cls(
            eid=str(obj.event_id),  # Get eid from the ORM object
            description=description  # Set description manually
        )
