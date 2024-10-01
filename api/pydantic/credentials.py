from pydantic import BaseModel, ConfigDict

class CredentialsBase(BaseModel):
    user_id: str

class CredentialsCreate(CredentialsBase):
    hashed_password: str

class CredentialsDB(CredentialsBase):
    credential_id: int

    model_config = ConfigDict(from_attributes=True)