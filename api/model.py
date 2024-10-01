from sqlalchemy import create_engine, Column, UUID, String, ForeignKey, DateTime, Text, LargeBinary, Boolean, Table
from sqlalchemy.orm import relationship, backref, Mapped
from sqlalchemy.sql import func
from database import Base
import uuid

# Association Table

person_lab = Table(
    'person_lab', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey(
        'people.user_id'), primary_key=True),
    Column('lab_id', UUID(as_uuid=True), ForeignKey(
        'labs.lab_id'), primary_key=True),
    Column('role', String(64))
)

person_project = Table(
    'person_project', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey(
        'people.user_id'), primary_key=True),
    Column('project_id', UUID(as_uuid=True), ForeignKey(
        'projects.project_id'), primary_key=True),
    Column('role', String(64))
)

# Tables


class Lab(Base):
    __tablename__ = 'labs'

    lab_id = Column(UUID(as_uuid=True), primary_key=True)
    lab_name = Column(String(100), nullable=False)
    image_high = Column(LargeBinary)
    image_low = Column(LargeBinary)
    body = Column(Text)

    # Relationships back populating
    projects: Mapped[list['Project']] = relationship(back_populates="lab")
    publications: Mapped[list['Publication']
                         ] = relationship(back_populates="lab")
    news: Mapped[list['News']] = relationship(back_populates="lab")
    events: Mapped[list['Event']] = relationship(back_populates="lab")


class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(UUID(as_uuid=True), primary_key=True)
    project_name = Column(String(100), nullable=False)
    image_high = Column(LargeBinary)
    image_low = Column(LargeBinary)
    body = Column(Text)

    # Foreign Keys
    lab_id = Column(UUID(as_uuid=True), ForeignKey('labs.lab_id'))

    # Relationships back populating
    lab: Mapped['Lab'] = relationship(back_populates="projects")
    news: Mapped[list['News']] = relationship(back_populates="project")
    events: Mapped[list['Event']] = relationship(back_populates="project")


class Publication(Base):
    __tablename__ = 'publications'

    publication_id = Column(UUID(as_uuid=True), primary_key=True)
    publication_name = Column(String(100), nullable=False)
    image_high = Column(LargeBinary)
    image_low = Column(LargeBinary)
    body = Column(Text)
    url = Column(Text)

    # Foreign Keys
    lab_id = Column(UUID(as_uuid=True), ForeignKey('labs.lab_id'))

    # Relationships back populating
    lab: Mapped['Lab'] = relationship(back_populates="publications")
    news: Mapped[list['News']] = relationship(back_populates="publication")
    events: Mapped[list['Event']] = relationship(back_populates="publication")


class News(Base):
    __tablename__ = 'news'

    news_id = Column(UUID(as_uuid=True), primary_key=True)
    news_name = Column(String(100), nullable=False)
    image_high = Column(LargeBinary)
    image_low = Column(LargeBinary)
    body = Column(Text)
    date = Column(DateTime, default=func.now())
    posted = Column(Boolean)

    # Foreign Keys
    lab_id = Column(UUID(as_uuid=True), ForeignKey(
        'labs.lab_id'), nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey(
        'projects.project_id'), nullable=True)
    publication_id = Column(UUID(as_uuid=True), ForeignKey(
        'publications.publication_id'), nullable=True)

    # Relationships back populating
    lab: Mapped['Lab'] = relationship(back_populates="news")
    project: Mapped['Project'] = relationship(back_populates="news")
    publication: Mapped['Publication'] = relationship(back_populates="news")


class Event(Base):
    __tablename__ = 'events'

    event_id = Column(UUID(as_uuid=True), primary_key=True)
    event_name = Column(String(100), nullable=False)
    image_high = Column(LargeBinary)
    image_low = Column(LargeBinary)
    body = Column(Text)
    location = Column(String(100))
    date_start = Column(DateTime, default=func.now())
    date_end = Column(DateTime)

    # Foreign Keys
    lab_id = Column(UUID(as_uuid=True), ForeignKey(
        'labs.lab_id'), nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey(
        'projects.project_id'), nullable=True)
    publication_id = Column(UUID(as_uuid=True), ForeignKey(
        'publications.publication_id'), nullable=True)

    # Relationships back populating
    lab: Mapped['Lab'] = relationship(back_populates="events")
    project: Mapped['Project'] = relationship(back_populates="events")
    publication: Mapped['Publication'] = relationship(back_populates="events")


class UserCredentials(Base):
    __tablename__ = 'user_credentials'

    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'people.user_id'), primary_key=True)
    password_hash = Column(String(255), nullable=False)

    # Relationship
    person: Mapped['Person'] = relationship(backref=backref(
        "user_credentials", uselist=False))


class Person(Base):
    __tablename__ = 'people'

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    full_name = Column(String(100), nullable=False)
    image_high = Column(LargeBinary)
    image_low = Column(LargeBinary)
    gmail = Column(String(100))
    highest_role = Column(String(100))
    admin = Column(Boolean)
    token = Column(String(100))

    # Many-to-Many relationships
    # backref = not needed in lab and project
    labs: Mapped[list['Lab']] = relationship(secondary=person_lab,
                                             backref=backref('people', lazy='dynamic'))
    projects: Mapped[list['Project']] = relationship(
        secondary=person_project, backref=backref('people', lazy='dynamic'))
