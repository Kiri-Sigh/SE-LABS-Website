from pydantic import BaseModel, ConfigDict

class PersonProjectBase(BaseModel):
    user_id: str
    project_id: str
    role: str

class PersonProjectDB(PersonProjectBase):
    model_config = ConfigDict(from_attributes=True)