from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .people import People
from .project import Project

class PersonProject(Base):
    __tablename__ = "person_project"

    user_id: Mapped[str] = mapped_column(ForeignKey("people.user_id"), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.project_id"), primary_key=True)
    role: Mapped[str]

    person: Mapped["People"] = relationship(back_populates="person_projects")
    project: Mapped["Project"] = relationship(back_populates="person_projects")