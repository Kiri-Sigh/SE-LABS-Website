from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from uuid import uuid4

from ..database import Base
from .person_lab import PersonLab
from .news import News
from .event import Events
from .project import Project
from .publication import Publication

class Lab(Base):
    __tablename__ = "lab"

    lab_id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    lab_name: Mapped[str]
    image_high: Mapped[bytes]
    image_low: Mapped[Optional[bytes]]
    body: Mapped[str]

    person_labs: Mapped[List["PersonLab"]] = relationship(back_populates="lab")
    news: Mapped[List["News"]] = relationship(back_populates="lab")
    events: Mapped[List["Events"]] = relationship(back_populates="lab")
    projects: Mapped[List["Project"]] = relationship(back_populates="lab")
    publications: Mapped[List["Publication"]] = relationship(back_populates="lab")