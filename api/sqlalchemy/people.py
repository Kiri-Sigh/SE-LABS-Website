from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from uuid import uuid4

from ..database import Base
from .credentials import Credentials
from .person_lab import PersonLab
from .person_project import PersonProject

class People(Base):
    __tablename__ = "people"

    user_id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    fullname: Mapped[str]
    image_high: Mapped[bytes]
    image_low: Mapped[Optional[bytes]]
    gmail: Mapped[str]
    token: Mapped[str]

    credentials: Mapped["Credentials"] = relationship(back_populates="user", uselist=False)
    person_labs: Mapped[List["PersonLab"]] = relationship(back_populates="person")
    person_projects: Mapped[List["PersonProject"]] = relationship(back_populates="person")