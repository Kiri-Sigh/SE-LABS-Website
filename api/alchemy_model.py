from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, LargeBinary, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    image = Column(LargeBinary)
    is_approve = Column(Boolean, nullable=False)

    laboratories = relationship("Laboratory", secondary="laboratory_news", back_populates="news")
    researches = relationship("Research", secondary="research_news", back_populates="news")

class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    location = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_approve = Column(Boolean, nullable=False)

    laboratories = relationship("Laboratory", secondary="laboratory_event", back_populates="events")
    researches = relationship("Research", secondary="research_event", back_populates="events")

class Publication(Base):
    __tablename__ = "publication"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    image = Column(LargeBinary)

    laboratory_id = Column(Integer, ForeignKey("laboratory.id"))
    laboratory = relationship("Laboratory", back_populates="publications")

class Researcher(Base):
    __tablename__ = "researcher"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    image = Column(LargeBinary)

    laboratories = relationship("Laboratory", secondary="researcher_laboratory", back_populates="researchers")
    researches = relationship("Research", secondary="researcher_research", back_populates="researchers")

class Research(Base):
    __tablename__ = "research"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    image = Column(LargeBinary)

    laboratory_id = Column(Integer, ForeignKey("laboratory.id"))
    laboratory = relationship("Laboratory", back_populates="researches")
    researchers = relationship("Researcher", secondary="researcher_research", back_populates="researches")
    news = relationship("News", secondary="research_news", back_populates="researches")
    events = relationship("Event", secondary="research_event", back_populates="researches")

class Laboratory(Base):
    __tablename__ = "laboratory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    image = Column(LargeBinary)

    news = relationship("News", secondary="laboratory_news", back_populates="laboratories")
    events = relationship("Event", secondary="laboratory_event", back_populates="laboratories")
    researches = relationship("Research", back_populates="laboratory")
    publications = relationship("Publication", back_populates="laboratory")
    researchers = relationship("Researcher", secondary="researcher_laboratory", back_populates="laboratories")

class ResearcherResearch(Base):
    __tablename__ = "researcher_research"

    researcher_id = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
    research_id = Column(Integer, ForeignKey("research.id"), primary_key=True)

class ResearcherLaboratory(Base):
    __tablename__ = "researcher_laboratory"

    researcher_id = Column(Integer, ForeignKey("researcher.id"), primary_key=True)
    laboratory_id = Column(Integer, ForeignKey("laboratory.id"), primary_key=True)

class LaboratoryNews(Base):
    __tablename__ = "laboratory_news"

    laboratory_id = Column(Integer, ForeignKey("laboratory.id"), primary_key=True)
    news_id = Column(Integer, ForeignKey("news.id"), primary_key=True)
    
class LaboratoryEvent(Base):
    __tablename__ = "laboratory_event"

    laboratory_id = Column(Integer, ForeignKey("laboratory.id"), primary_key=True)
    event_id = Column(Integer, ForeignKey("event.id"), primary_key=True)

class ResearchNews(Base):
    __tablename__ = "research_news"

    research_id = Column(Integer, ForeignKey("research.id"), primary_key=True)
    news_id = Column(Integer, ForeignKey("news.id"), primary_key=True)

class ResearchEvent(Base):
    __tablename__ = "research_event"

    research_id = Column(Integer, ForeignKey("research.id"), primary_key=True)
    event_id = Column(Integer, ForeignKey("event.id"), primary_key=True)