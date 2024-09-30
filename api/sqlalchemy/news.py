from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from uuid import uuid4

from ..database import Base

if __name__ == "__main__":
    from .lab import Lab
    from .project import Project
    from .publication import Publication

class News(Base):
    __tablename__ = "news"

    news_id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    news_name: Mapped[str]
    image_high: Mapped[bytes]
    image_low: Mapped[Optional[bytes]]
    body: Mapped[str]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    posted: Mapped[bool] = mapped_column(Boolean, default=False)
    lab_id: Mapped[Optional[str]] = mapped_column(ForeignKey("lab.lab_id"))
    project_id: Mapped[Optional[str]] = mapped_column(ForeignKey("project.project_id"))
    publication_id: Mapped[Optional[str]] = mapped_column(ForeignKey("publication.publication_id"))

    lab: Mapped[Optional["Lab"]] = relationship(back_populates="news")
    project: Mapped[Optional["Project"]] = relationship(back_populates="news")
    publication: Mapped[Optional["Publication"]] = relationship(back_populates="news")