from pydantic import BaseModel, ConfigDict

class PersonLabBase(BaseModel):
    user_id: str
    lab_id: str
    role: str

class PersonLabDB(PersonLabBase):
    model_config = ConfigDict(from_attributes=True)

    