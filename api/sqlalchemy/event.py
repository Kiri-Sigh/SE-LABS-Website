from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from uuid import uuid4

from ..database import Base
from .lab import Lab
from .project import Project
from .publication import Publication

class Events(Base):
    __tablename__ = "events"

    event_id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    event_name: Mapped[str]
    image_high: Mapped[bytes]
    image_low: Mapped[Optional[bytes]]
    body: Mapped[str]
    location: Mapped[str]
    date_start: Mapped[datetime]
    date_end: Mapped[datetime]
    posted: Mapped[bool] = mapped_column(Boolean, default=False)
    lab_id: Mapped[Optional[str]] = mapped_column(ForeignKey("lab.lab_id"))
    project_id: Mapped[Optional[str]] = mapped_column(ForeignKey("project.project_id"))
    publication_id: Mapped[Optional[str]] = mapped_column(ForeignKey("publication.publication_id"))

    lab: Mapped[Optional["Lab"]] = relationship(back_populates="events")
    project: Mapped[Optional["Project"]] = relationship(back_populates="events")
    publication: Mapped[Optional["Publication"]] = relationship(back_populates="events")