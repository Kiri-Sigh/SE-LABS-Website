from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

from .ult.position import Position
from .ult.LRE02 import LRE02
from .ult.RRE01 import RRE01

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class AU01(BaseModel):
    UID: UUID
    name: str
    gmail: EmailStr
    position: Position
    token: str
    active: bool = True
    Laboratories: list[LRE02]
    Researches: list[RRE01]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj, token: str):
        return cls(
            UID=obj.user_id,
            name=obj.full_name,
            gmail=obj.gmail,
            position=obj.highest_role,
            token=token,
            active=obj.active,
            Laboratories=[LRE02.from_orm(lab) for lab in obj.labs],
            Researches=[RRE01.from_orm(research) for research in obj.researches]
        )

class AU02(AU01):
    hashed_password: str

class AuthUser(BaseModel):
    Researcher: AU01

class AuthUserWithPassword(BaseModel):
    Researcher: AU02