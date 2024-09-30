from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from uuid import uuid4

from ..database import Base

if __name__ == "__main__":
    from .lab import Lab
    from .person_project import PersonProject
    from .news import News
    from .event import Events

class Publication(Base):
    __tablename__ = "publication"

    publication_id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    publication_name: Mapped[str]
    image_high: Mapped[bytes]
    image_low: Mapped[Optional[bytes]]
    body: Mapped[str]
    publication_link: Mapped[str]
    lab_id: Mapped[str] = mapped_column(ForeignKey("lab.lab_id"))

    lab: Mapped["Lab"] = relationship(back_populates="publications")
    news: Mapped[List["News"]] = relationship(back_populates="publication")
    events: Mapped[List["Events"]] = relationship(back_populates="publication")