from pydantic import BaseModel, EmailStr

class RL01(BaseModel):
    mail: EmailStr
    password: str