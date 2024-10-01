from .database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

class Credentials(Base):
    __tablename__ = "credentials"

    credential_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("people.user_id"), unique=True)
    hashed_password: Mapped[str]

    user: Mapped["People"] = relationship(back_populates="credentials")

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

class PersonLab(Base):
    __tablename__ = "person_lab"

    user_id: Mapped[str] = mapped_column(ForeignKey("people.user_id"), primary_key=True)
    lab_id: Mapped[str] = mapped_column(ForeignKey("lab.lab_id"), primary_key=True)
    role: Mapped[str]

    person: Mapped["People"] = relationship(back_populates="person_labs")
    lab: Mapped["Lab"] = relationship(back_populates="person_labs")

class PersonProject(Base):
    __tablename__ = "person_project"

    user_id: Mapped[str] = mapped_column(ForeignKey("people.user_id"), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("project.project_id"), primary_key=True)
    role: Mapped[str]

    person: Mapped["People"] = relationship(back_populates="person_projects")
    project: Mapped["Project"] = relationship(back_populates="person_projects")

class Project(Base):
    __tablename__ = "project"

    project_id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    project_name: Mapped[str]
    image_high: Mapped[bytes]
    image_low: Mapped[Optional[bytes]]
    body: Mapped[str]
    lab_id: Mapped[str] = mapped_column(ForeignKey("lab.lab_id"))

    lab: Mapped["Lab"] = relationship(back_populates="projects")
    person_projects: Mapped[List["PersonProject"]] = relationship(back_populates="project")
    news: Mapped[List["News"]] = relationship(back_populates="project")
    events: Mapped[List["Events"]] = relationship(back_populates="project")

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