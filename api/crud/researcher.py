from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from ..models.model import Researcher
from ..schemas.core.researcher import ResearcherCreate, ResearcherDB

async def create_researcher(db: AsyncSession, researcher_create: ResearcherCreate) -> ResearcherDB:
    try:
        new_researcher = Researcher(**researcher_create.model_dump())
        db.add(new_researcher)
        await db.commit()
        await db.refresh(new_researcher)
        return new_researcher
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_researcher(db: AsyncSession, researcher_id: int) -> ResearcherDB:
    try:
        result = await db.execute(select(Researcher).filter(Researcher.researcher_id == researcher_id))
        researcher = result.scalars().first()
        if not researcher:
            raise HTTPException(status_code=404, detail="Researcher not found")
        return researcher
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_researchers(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ResearcherDB]:
    try:
        result = await db.execute(select(Researcher).offset(skip).limit(limit))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_researcher(db: AsyncSession, researcher_id: int, researcher_update: ResearcherCreate) -> ResearcherDB:
    try:
        result = await db.execute(select(Researcher).filter(Researcher.researcher_id == researcher_id))
        researcher = result.scalars().first()
        if not researcher:
            raise HTTPException(status_code=404, detail="Researcher not found")

        for key, value in researcher_update.model_dump().items():
            setattr(researcher, key, value)

        await db.commit()
        await db.refresh(researcher)
        return researcher
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_researcher(db: AsyncSession, researcher_id: int) -> dict:
    try:
        result = await db.execute(select(Researcher).filter(Researcher.researcher_id == researcher_id))
        researcher = result.scalars().first()
        if not researcher:
            raise HTTPException(status_code=404, detail="Researcher not found")

        await db.delete(researcher)
        await db.commit()
        return {"message": "Researcher deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")