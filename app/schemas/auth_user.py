from pydantic import BaseModel, EmailStr
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
    uid: UUID
    name: str
    gmail: EmailStr
    position: Position
    token: str
    Laboratories: list[LRE02]
    Researches: list[RRE01]

class AU02(AU01):
    hashed_password: str

class AuthUser(BaseModel):
    Researcher: AU01

class AuthUserWithPassword(BaseModel):
    Researcher: AU02