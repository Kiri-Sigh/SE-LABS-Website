from sqlalchemy.ext.asyncio import AsyncSession

from ..models.model import Researcher
from ..schemas.core.researcher import ResearcherCreate, ResearcherDB

async def create_researcher(db: AsyncSession, researcher_create: ResearcherCreate) -> ResearcherDB:
    # Create a new researcher instance
    new_researcher = Researcher(
        **researcher_create.model_dump()
    )

    # Add the new researcher to the database
    await db.add(new_researcher)
    await db.commit()

    # Refresh the new researcher to ensure it reflects the current state in the database
    await db.refresh(new_researcher)

    return new_researcher

async def get_researcher(db: AsyncSession, researcher_id: int) -> ResearcherDB:
    # Fetch the researcher from the database
    # researcher = db.query(Researcher).filter(Researcher.researcher_id == researcher_id).first()
    researcher = await db.execute(db.query(Researcher).filter(Researcher.researcher_id == researcher_id)).scalars().first()
    if not researcher:
        raise ValueError("Researcher not found")

    return researcher

async def get_researchers(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ResearcherDB]:
    # Fetch all researchers from the database
    # researchers = db.query(Researcher).offset(skip).limit(limit).all()
    researchers = await db.execute(db.query(Researcher).offset(skip).limit(limit)).schelars().all()

    return researchers

async def update_researcher(db: AsyncSession, researcher_id: int, researcher_update: ResearcherCreate) -> ResearcherDB:
    # Fetch the researcher to be updated
    # researcher = db.query(Researcher).filter(Researcher.researcher_id == researcher_id).first()
    researcher = await db.execute(db.query(Researcher).filter(Researcher.researcher_id == researcher_id)).scalars().first()
    if not researcher:
        raise ValueError("Researcher not found")

    # Update the researcher with the new data
    for key, value in researcher_update.dict().items():
        setattr(researcher, key, value)

    # Commit the changes
    await db.commit()

    # Refresh the researcher to ensure it reflects the current state in the database
    await db.refresh(researcher)

    return researcher

async def delete_researcher(db: AsyncSession, researcher_id: int) -> ResearcherDB:
    # Fetch the researcher to be deleted
    # researcher = db.query(Researcher).filter(Researcher.researcher_id == researcher_id).first()
    researcher = await db.execute(db.query(Researcher).filter(Researcher.researcher_id == researcher_id)).scalars().first()
    if not researcher:
        raise ValueError("Researcher not found")

    # Delete the researcher from the database
    await db.delete(researcher)
    await db.commit()

    return researcher