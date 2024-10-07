from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from uuid import uuid4, UUID
from pydantic import HttpUrl

from ..models.model import Publication, News, Event, Research
from ..schemas.core.publication import PublicationCreate, PublicationDB

async def create_publication(db: AsyncSession, publication_create: PublicationCreate) -> PublicationDB:
    try:
        new_publication = Publication(publication_id=uuid4(), **publication_create.model_dump())
        db.add(new_publication)
        await db.commit()
        await db.refresh(new_publication)
        return new_publication
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_publication(db: AsyncSession, publication_id: UUID) -> PublicationDB:
    try:
        result = await db.execute(select(Publication).filter(Publication.publication_id == publication_id))
        publication = result.scalars().first()
        if not publication:
            raise HTTPException(status_code=404, detail="Publication not found")
        return publication
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_publications(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[PublicationDB]:
    try:
        result = await db.execute(select(Publication).offset(skip).limit(limit))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_publication(db: AsyncSession, publication_id: UUID, publication_update: PublicationCreate) -> PublicationDB:
    try:
        result = await db.execute(select(Publication).filter(Publication.publication_id == publication_id))
        publication = result.scalars().first()
        if not publication:
            raise HTTPException(status_code=404, detail="Publication not found")

        for key, value in publication_update.model_dump().items():
            setattr(publication, key, value)

        await db.commit()
        await db.refresh(publication)
        return publication
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def migrate_research_to_publication(db: AsyncSession, research_id: UUID) -> PublicationDB:
    try:
        result = await db.execute(select(Research).filter(Research.research_id == research_id))
        research = result.scalars().first()
        if not research:
            raise HTTPException(status_code=404, detail="Research not found")

        publication_create = PublicationCreate(
            publication_name=research.research_name,
            body=research.body,
            publication_link=HttpUrl('https://example.com'),
            lab_id=research.lab_id
        )

        new_publication = Publication(
            publication_id=uuid4(),
            **publication_create.model_dump(),
            image_high=research.image_high,
            image_low=research.image_low
        )
        db.add(new_publication)

        await db.execute(update(News).where(News.research_id == research_id).values(
            research_id=None, publication_id=new_publication.publication_id
        ))
        await db.execute(update(Event).where(Event.research_id == research_id).values(
            research_id=None, publication_id=new_publication.publication_id
        ))

        await db.delete(research)
        await db.commit()
        await db.refresh(new_publication)
        return new_publication
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_publication(db: AsyncSession, publication_id: UUID) -> dict:
    try:
        result = await db.execute(select(Publication).filter(Publication.publication_id == publication_id))
        publication = result.scalars().first()
        if not publication:
            raise HTTPException(status_code=404, detail="Publication not found")

        await db.delete(publication)
        await db.commit()
        return {"message": "Publication deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")