from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .people import People
from .lab import Lab

class PersonLab(Base):
    __tablename__ = "person_lab"

    user_id: Mapped[str] = mapped_column(ForeignKey("people.user_id"), primary_key=True)
    lab_id: Mapped[str] = mapped_column(ForeignKey("lab.lab_id"), primary_key=True)
    role: Mapped[str]

    person: Mapped["People"] = relationship(back_populates="person_labs")
    lab: Mapped["Lab"] = relationship(back_populates="person_labs")