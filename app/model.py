from sqlalchemy import Column, String, ForeignKey, DateTime, Text, LargeBinary, Boolean
from sqlalchemy import Enum as sqlalchemy_enum
from sqlalchemy.orm import relationship, backref, Mapped, mapped_column
from sqlalchemy.sql import func
from typing import List, Optional
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from PIL import Image
import io

from database import Base
from schemas.ult.position import Position

class person_lab(Base):
    __tablename__ = 'person_lab'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('people.user_id'), primary_key=True)
    lab_id: Mapped[UUID] = mapped_column(ForeignKey('labs.lab_id'), primary_key=True)
    role: Mapped[Position] = mapped_column(sqlalchemy_enum(Position, name="position_enum"), nullable=False)

class person_research(Base):
    __tablename__ = 'person_research'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('people.user_id'), primary_key=True)
    research_id: Mapped[UUID] = mapped_column(ForeignKey('researches.research_id'), primary_key=True)
    role: Mapped[Position] = mapped_column(sqlalchemy_enum(Position, name="position_enum"), nullable=False)

class Laboratory(Base):
    __tablename__ = 'labs'

    lab_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    lab_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[str] = mapped_column(Text)

    # Relationships
    researches: Mapped[List['Research']] = relationship(back_populates="lab")
    publications: Mapped[List['Publication']] = relationship(back_populates="lab")
    news: Mapped[List['News']] = relationship(back_populates="lab")
    events: Mapped[List['Event']] = relationship(back_populates="lab")

class Research(Base):
    __tablename__ = 'researches'

    research_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    research_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[str] = mapped_column(Text)

    # Foreign Keys
    lab_id: Mapped[UUID] = mapped_column(ForeignKey('labs.lab_id'))

    # Relationships
    lab: Mapped['Laboratory'] = relationship(back_populates="researches")
    news: Mapped[List['News']] = relationship(back_populates="research")
    events: Mapped[List['Event']] = relationship(back_populates="research")

class Publication(Base):
    __tablename__ = 'publications'

    publication_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    publication_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)

    # Foreign Keys
    lab_id: Mapped[UUID] = mapped_column(ForeignKey('labs.lab_id'))

    # Relationships
    lab: Mapped['Laboratory'] = relationship(back_populates="publications")
    news: Mapped[List['News']] = relationship(back_populates="publication")
    events: Mapped[List['Event']] = relationship(back_populates="publication")

class News(Base):
    __tablename__ = 'news'

    news_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    news_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    posted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Foreign Keys
    lab_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('labs.lab_id'), nullable=True)
    research_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('researches.research_id'), nullable=True)
    publication_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('publications.publication_id'), nullable=True)

    # Relationships
    lab: Mapped[Optional['Laboratory']] = relationship(back_populates="news")
    research: Mapped[Optional['Research']] = relationship(back_populates="news")
    publication: Mapped[Optional['Publication']] = relationship(back_populates="news")

class Event(Base):
    __tablename__ = 'events'

    event_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    event_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    body: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String(100))
    date_start: Mapped[datetime] = mapped_column(DateTime, default=func.now() + timedelta(days=1))
    date_end: Mapped[datetime] = mapped_column(DateTime, default=lambda: func.now() + timedelta(days=1, hours=3))
    posted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Foreign Keys
    lab_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('labs.lab_id'), nullable=True)
    research_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('researches.research_id'), nullable=True)
    publication_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('publications.publication_id'), nullable=True)

    # Relationships
    lab: Mapped[Optional['Laboratory']] = relationship(back_populates="events")
    research: Mapped[Optional['Research']] = relationship(back_populates="events")
    publication: Mapped[Optional['Publication']] = relationship(back_populates="events")

    @staticmethod
    def process_image(image: bytes, max_size: tuple = (800, 600)) -> bytes:
        img = Image.open(io.BytesIO(image))
        img = img.convert('RGB')  # Ensure the image is in RGB mode
        img.thumbnail(max_size)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return buffer.getvalue()

    def set_images(self, image: bytes):
        self.image_high = self.process_image(image, (800, 600))
        self.image_low = self.process_image(image, (400, 300))

class UserCredentials(Base):
    __tablename__ = 'user_credentials'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('people.user_id'), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship
    person: Mapped['Researcher'] = relationship("Researcher", back_populates="user_credentials")

class Researcher(Base):
    __tablename__ = 'people'

    user_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_high: Mapped[bytes] = mapped_column(LargeBinary)
    image_low: Mapped[bytes] = mapped_column(LargeBinary)
    gmail: Mapped[str] = mapped_column(String(100))
    highest_role: Mapped[Position] = mapped_column(sqlalchemy_enum(Position, name="position_enum"), nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship
    user_credentials: Mapped['UserCredentials'] = relationship("UserCredentials", back_populates="person", uselist=False)

    # Many-to-Many relationships
    labs: Mapped[List['Laboratory']] = relationship(secondary=person_lab.__table__, backref=backref('people', lazy='dynamic'))
    researches: Mapped[List['Research']] = relationship(secondary=person_research.__table__, backref=backref('researchers', lazy='dynamic'))