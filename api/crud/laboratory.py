from sqlalchemy.ext.asyncio import AsyncSession

from ..models.model import Laboratory
from ..schemas.core.laboratory import LaboratoryCreate, LaboratoryDB

async def create_laboratory(db: AsyncSession, laboratory_create: LaboratoryCreate) -> LaboratoryDB:
    # Create a new laboratory instance
    new_laboratory = Laboratory(
        **laboratory_create.model_dump()
    )

    # Add the new laboratory to the database
    await db.add(new_laboratory)
    await db.commit()

    # Refresh the new laboratory to ensure it reflects the current state in the database
    await db.refresh(new_laboratory)

    return new_laboratory

async def get_laboratory(db: AsyncSession, laboratory_id: int) -> LaboratoryDB:
    # Fetch the laboratory from the database
    # laboratory = db.query(Laboratory).filter(Laboratory.laboratory_id == laboratory_id).first()
    laboratory = await db.execute(db.query(Laboratory).filter(Laboratory.laboratory_id == laboratory_id)).scalars().first()
    if not laboratory:
        raise ValueError("Laboratory not found")

    return laboratory

async def get_laboratories(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[LaboratoryDB]:
    # Fetch all laboratories from the database
    # laboratories = db.query(Laboratory).offset(skip).limit(limit).all()
    laboratories = await db.execute(db.query(Laboratory).offset(skip).limit(limit)).schelars().all()

    return laboratories

async def update_laboratory(db: AsyncSession, laboratory_id: int, laboratory_update: LaboratoryCreate) -> LaboratoryDB:
    # Fetch the laboratory to be updated
    # laboratory = db.query(Laboratory).filter(Laboratory.laboratory_id == laboratory_id).first()
    laboratory = await db.execute(db.query(Laboratory).filter(Laboratory.laboratory_id == laboratory_id)).scalars().first()
    if not laboratory:
        raise ValueError("Laboratory not found")

    # Update the laboratory with the new data
    for key, value in laboratory_update.dict().items():
        setattr(laboratory, key, value)

    # Commit the changes
    await db.commit()

    # Refresh the laboratory to ensure it reflects the current state in the database
    await db.refresh(laboratory)

    return laboratory

async def delete_laboratory(db: AsyncSession, laboratory_id: int) -> LaboratoryDB:
    # Fetch the laboratory to be deleted
    laboratory = db.query(Laboratory).filter(Laboratory.laboratory_id == laboratory_id).first()
    if not laboratory:
        raise ValueError("Laboratory not found")

    # Delete the laboratory from the database
    await db.delete(laboratory)
    await db.commit()

    return laboratory