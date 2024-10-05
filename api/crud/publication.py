from sqlalchemy.orm import Session
from uuid import uuid4, UUID
from pydantic import HttpUrl

from ..models.model import Publication, News, Event, Research
from ..schemas.core.publication import PublicationCreate, PublicationDB

def create_publication(db: Session, publication_create: PublicationCreate) -> PublicationDB:
    # Create a new publication instance
    new_publication = Publication(
        publication_id=uuid4(),
        **publication_create.model_dump()
    )

    # Add the new publication to the database
    db.add(new_publication)
    db.commit()

    # Refresh the new publication to ensure it reflects the current state in the database
    db.refresh(new_publication)

    return new_publication

def get_publication(db: Session, publication_id: UUID) -> PublicationDB:
    # Fetch the publication from the database
    publication = db.query(Publication).filter(Publication.publication_id == publication_id).first()
    if not publication:
        raise ValueError("Publication not found")

    return publication

def get_publications(db: Session, skip: int = 0, limit: int = 100) -> list[PublicationDB]:
    # Fetch all publications from the database
    publications = db.query(Publication).offset(skip).limit(limit).all()

    return publications

def update_publication(db: Session, publication_id: UUID, publication_update: PublicationCreate) -> PublicationDB:
    # Fetch the publication to be updated
    publication = db.query(Publication).filter(Publication.publication_id == publication_id).first()
    if not publication:
        raise ValueError("Publication not found")

    # Update the publication with the new data
    for key, value in publication_update.dict().items():
        setattr(publication, key, value)

    # Commit the changes
    db.commit()

    # Refresh the publication to ensure it reflects the current state in the database
    db.refresh(publication)

    return publication

def migrate_research_to_publication(db: Session, research_id: UUID) -> PublicationDB:
    # Fetch the research to be deleted
    research = db.query(Research).filter(Research.research_id == research_id).first()
    if not research:
        raise ValueError("Research not found")

    # Create a PublicationCreate instance
    publication_create = PublicationCreate(
        publication_name=research.research_name,
        body=research.body,
        publication_link=HttpUrl('https://example.com'),  # Default URL, consider making this a parameter
        lab_id=research.lab_id
    )

    # Create a new publication in the database
    new_publication = Publication(
        publication_id=uuid4(),
        **publication_create.model_dump(),
        image_high=research.image_high,
        image_low=research.image_low
    )
    db.add(new_publication)

    # Update associated news
    db.query(News).filter(News.research_id == research_id).update(
        {"research_id": None, "publication_id": new_publication.publication_id}
    )

    # Update associated events
    db.query(Event).filter(Event.research_id == research_id).update(
        {"research_id": None, "publication_id": new_publication.publication_id}
    )

    # Delete the research
    db.delete(research)

    # Commit the changes
    db.commit()

    # Refresh the new publication to ensure it reflects the current state in the database
    db.refresh(new_publication)

    return new_publication

def delete_publication(db: Session, publication_id: UUID) -> PublicationDB:
    # Fetch the publication to be deleted
    publication = db.query(Publication).filter(Publication.publication_id == publication_id).first()
    if not publication:
        raise ValueError("Publication not found")

    # Delete the publication
    db.delete(publication)
    db.commit()

    return publication