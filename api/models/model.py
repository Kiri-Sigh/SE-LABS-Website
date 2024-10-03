from sqlalchemy import Column, UUID, String, ForeignKey, DateTime, Text, LargeBinary, Boolean, Table
from sqlalchemy.orm import relationship, backref, Mapped, mapped_column
from sqlalchemy.sql import func
from typing import List, Optional
import datetime
import uuid


# from ..database.database import Base
from ..database import database as database

person_lab = Table(
    'person_lab', database.Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('people.user_id'), primary_key=True),
    Column('lab_id', UUID(as_uuid=True), ForeignKey('labs.lab_id'), primary_key=True),
    Column('role', String(64))
)

person_research = Table(
    'person_research', database.Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('people.user_id'), primary_key=True),
    Column('research_id', UUID(as_uuid=True), ForeignKey('researches.research_id'), primary_key=True),
    Column('role', String(64))
)

class Laboratory(database.Base):
    __tablename__ = 'labs'

    lab_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    lab_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[str] = mapped_column(Text)

    # Relationships
    researches: Mapped[List['Research']] = relationship(back_populates="lab")
    publications: Mapped[List['Publication']] = relationship(back_populates="lab")
    news: Mapped[List['News']] = relationship(back_populates="lab")
    events: Mapped[List['Event']] = relationship(back_populates="lab")

class Research(database.Base):
    __tablename__ = 'researches'

    research_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    research_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[str] = mapped_column(Text)

    # Foreign Keys
    lab_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('labs.lab_id'))

    # Relationships
    lab: Mapped['Laboratory'] = relationship(back_populates="researches")
    news: Mapped[List['News']] = relationship(back_populates="research")
    events: Mapped[List['Event']] = relationship(back_populates="research")

class Publication(database.Base):
    __tablename__ = 'publications'

    publication_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    publication_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)

    # Foreign Keys
    lab_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('labs.lab_id'))

    # Relationships
    lab: Mapped['Laboratory'] = relationship(back_populates="publications")
    news: Mapped[List['News']] = relationship(back_populates="publication")
    events: Mapped[List['Event']] = relationship(back_populates="publication")

class News(database.Base):
    __tablename__ = 'news'

    news_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    news_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    posted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Foreign Keys
    lab_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('labs.lab_id'), nullable=True)
    research_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('researches.research_id'), nullable=True)
    publication_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('publications.publication_id'), nullable=True)

    # Relationships
    lab: Mapped[Optional['Laboratory']] = relationship(back_populates="news")
    research: Mapped[Optional['Research']] = relationship(back_populates="news")
    publication: Mapped[Optional['Publication']] = relationship(back_populates="news")

class Event(database.Base):
    __tablename__ = 'events'

    event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    event_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String(100))
    date_start: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now() + datetime.timedelta(days=1))
    date_end: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: func.now() + datetime.timedelta(days=1, hours=3))
    posted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Foreign Keys
    lab_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('labs.lab_id'), nullable=True)
    research_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('researches.research_id'), nullable=True)
    publication_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('publications.publication_id'), nullable=True)

    # Relationships
    lab: Mapped[Optional['Laboratory']] = relationship(back_populates="events")
    research: Mapped[Optional['Research']] = relationship(back_populates="events")
    publication: Mapped[Optional['Publication']] = relationship(back_populates="events")

class UserCredentials(database.Base):
    __tablename__ = 'user_credentials'

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('people.user_id'), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship
    person: Mapped['Person'] = relationship(backref=backref("user_credentials", uselist=False))

class Person(database.Base):
    __tablename__ = 'people'

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    gmail: Mapped[str] = mapped_column(String(100))
    highest_role: Mapped[str] = mapped_column(String(100))
    admin: Mapped[bool] = mapped_column(Boolean)
    token: Mapped[Optional[str]] = mapped_column(String(100))

    # Many-to-Many relationships
    labs: Mapped[List['Laboratory']] = relationship(secondary=person_lab, backref=backref('people', lazy='dynamic'))
    researches: Mapped[List['Research']] = relationship(secondary=person_research, backref=backref('people', lazy='dynamic'))