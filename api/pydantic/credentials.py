from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, HttpUrl, ConfigDict
from typing import Optional, List
from uuid import UUID, uuid4


class CredentialsBase(BaseModel):
    user_id: str

class CredentialsCreate(CredentialsBase):
    hashed_password: str

class CredentialsDB(CredentialsBase):
    credential_id: int

    model_config = ConfigDict(from_attributes=True)