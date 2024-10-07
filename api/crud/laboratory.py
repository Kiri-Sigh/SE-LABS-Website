from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from ..models.model import Laboratory
from ..schemas.core.laboratory import LaboratoryCreate, LaboratoryDB

async def create_laboratory(db: AsyncSession, laboratory_create: LaboratoryCreate) -> LaboratoryDB:
    try:
        new_laboratory = Laboratory(**laboratory_create.model_dump())
        db.add(new_laboratory)
        await db.commit()
        await db.refresh(new_laboratory)
        return new_laboratory
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_laboratory(db: AsyncSession, laboratory_id: int) -> LaboratoryDB:
    try:
        result = await db.execute(select(Laboratory).filter(Laboratory.laboratory_id == laboratory_id))
        laboratory = result.scalars().first()
        if not laboratory:
            raise HTTPException(status_code=404, detail="Laboratory not found")
        return laboratory
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_laboratories(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[LaboratoryDB]:
    try:
        result = await db.execute(select(Laboratory).offset(skip).limit(limit))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_laboratory(db: AsyncSession, laboratory_id: int, laboratory_update: LaboratoryCreate) -> LaboratoryDB:
    try:
        result = await db.execute(select(Laboratory).filter(Laboratory.laboratory_id == laboratory_id))
        laboratory = result.scalars().first()
        if not laboratory:
            raise HTTPException(status_code=404, detail="Laboratory not found")

        for key, value in laboratory_update.model_dump().items():
            setattr(laboratory, key, value)

        await db.commit()
        await db.refresh(laboratory)
        return laboratory
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_laboratory(db: AsyncSession, laboratory_id: int) -> dict:
    try:
        result = await db.execute(select(Laboratory).filter(Laboratory.laboratory_id == laboratory_id))
        laboratory = result.scalars().first()
        if not laboratory:
            raise HTTPException(status_code=404, detail="Laboratory not found")

        await db.delete(laboratory)
        await db.commit()
        return {"message": "Laboratory deleted successfully"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")