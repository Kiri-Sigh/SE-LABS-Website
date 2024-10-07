from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4, UUID
from pydantic import HttpUrl

from ..models.model import Publication, News, Event, Research
from ..schemas.core.publication import PublicationCreate, PublicationDB

async def create_publication(db: AsyncSession, publication_create: PublicationCreate) -> PublicationDB:
    # Create a new publication instance
    new_publication = Publication(
        publication_id=uuid4(),
        **publication_create.model_dump()
    )

    # Add the new publication to the database
    await db.add(new_publication)
    await db.commit()

    # Refresh the new publication to ensure it reflects the current state in the database
    await db.refresh(new_publication)

    return new_publication

async def get_publication(db: AsyncSession, publication_id: UUID) -> PublicationDB:
    # Fetch the publication from the database
    # publication = db.query(Publication).filter(Publication.publication_id == publication_id).first()
    publication = await db.execute(db.query(Publication).filter(Publication.publication_id == publication_id)).scalars().first()
    if not publication:
        raise ValueError("Publication not found")

    return publication

async def get_publications(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[PublicationDB]:
    # Fetch all publications from the database
    # publications = db.query(Publication).offset(skip).limit(limit).all()
    publications = await db.execute(db.query(Publication).offset(skip).limit(limit)).schelars().all()

    return publications

async def update_publication(db: AsyncSession, publication_id: UUID, publication_update: PublicationCreate) -> PublicationDB:
    # Fetch the publication to be updated
    # publication = db.query(Publication).filter(Publication.publication_id == publication_id).first()
    publication = await db.execute(db.query(Publication).filter(Publication.publication_id == publication_id)).scalars().first()
    if not publication:
        raise ValueError("Publication not found")

    # Update the publication with the new data
    for key, value in publication_update.model_dump().items():
        setattr(publication, key, value)

    # Commit the changes
    await db.commit()

    # Refresh the publication to ensure it reflects the current state in the database
    await db.refresh(publication)

    return publication

async def migrate_research_to_publication(db: AsyncSession, research_id: UUID) -> PublicationDB:
    # Fetch the research to be deleted
    # research = db.query(Research).filter(Research.research_id == research_id).first()
    research = await db.execute(db.query(Research).filter(Research.research_id == research_id)).scalars().first()
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
    await db.add(new_publication)

    # Update associated news
    # db.query(News).filter(News.research_id == research_id).update(
    #     {"research_id": None, "publication_id": new_publication.publication_id}
    # )
    await db.execute(db.query(News).filter(News.research_id == research_id).update(
        {"research_id": None, "publication_id": new_publication.publication_id}
    ))

    # Update associated events
    # db.query(Event).filter(Event.research_id == research_id).update(
    #     {"research_id": None, "publication_id": new_publication.publication_id}
    # )
    await db.execute(db.query(Event).filter(Event.research_id == research_id).update(
        {"research_id": None, "publication_id": new_publication.publication_id}
    ))

    # Delete the research
    await db.delete(research)

    # Commit the changes
    await db.commit()

    # Refresh the new publication to ensure it reflects the current state in the database
    await db.refresh(new_publication)

    return new_publication

async def delete_publication(db: AsyncSession, publication_id: UUID) -> PublicationDB:
    # Fetch the publication to be deleted
    # publication = db.query(Publication).filter(Publication.publication_id == publication_id).first()
    publication = await db.execute(db.query(Publication).filter(Publication.publication_id == publication_id)).scalars().first
    if not publication:
        raise ValueError("Publication not found")

    # Delete the publication
    await db.delete(publication)
    await db.commit()

    return publication