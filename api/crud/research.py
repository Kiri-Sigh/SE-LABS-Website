from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from ..models.model import Research
from ..schemas.core.research import ResearchCreate, ResearchDB

async def get_research(db: AsyncSession, research_id: int) -> ResearchDB:
    try:
        result = await db.execute(select(Research).filter(Research.research_id == research_id))
        research = result.scalars().first()
        if not research:
            raise HTTPException(status_code=404, detail="Research not found")
        return research
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_research_list(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ResearchDB]:
    try:
        result = await db.execute(select(Research).offset(skip).limit(limit))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def create_research(db: AsyncSession, research: ResearchCreate) -> ResearchDB:
    try:
        db_research = Research(**research.model_dump())
        db.add(db_research)
        await db.commit()
        await db.refresh(db_research)
        return db_research
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def edit_research(db: AsyncSession, research_id: int, research: ResearchCreate) -> ResearchDB:
    try:
        result = await db.execute(select(Research).filter(Research.research_id == research_id))
        db_research = result.scalars().first()
        if not db_research:
            raise HTTPException(status_code=404, detail="Research not found")

        for key, value in research.model_dump().items():
            if value is not None:
                setattr(db_research, key, value)

        await db.commit()
        await db.refresh(db_research)
        return db_research
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_research(db: AsyncSession, research_id: int) -> dict:
    try:
        result = await db.execute(select(Research).filter(Research.research_id == research_id))
        db_research = result.scalars().first()
        if not db_research:
            raise HTTPException(status_code=404, detail="Research not found")

        await db.delete(db_research)
        await db.commit()
        return {"message": "Research deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")