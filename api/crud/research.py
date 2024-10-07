from sqlalchemy.ext.asyncio import AsyncSession
from ..models.model import Research
from ..schemas.core.research import ResearchCreate, ResearchDB

async def get_research(db: AsyncSession, research_id: int) -> ResearchDB:
    # return db.query(Research).filter(Research.research_id == research_id).first()
    return db.execute(db.query(Research).filter(Research.research_id == research_id)).scalars().first()

async def get_research_list(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ResearchDB]:
    # return db.query(Research).offset(skip).limit(limit).all()
    return db.execute(db.query(Research).offset(skip).limit(limit)).scalars().all()

async def create_research(db: AsyncSession, research: ResearchCreate) -> ResearchDB:
    db_research = Research(**research.model_dump())
    await db.add(db_research)
    await db.commit()
    await db.refresh(db_research)
    return db_research

async def edit_research(db: AsyncSession, research_id: int, research: ResearchCreate) -> ResearchDB:
    # db_research = db.query(Research).filter(Research.research_id == research_id).first()
    db_research = await db.execute(db.query(Research).filter(Research.research_id == research_id)).scalars().first()
    if not db_research:
        return None
    for key, value in research.model_dump().items():
        if value is not None:
            setattr(db_research, key, value)
    await db.commit()
    await db.refresh(db_research)
    return db_research

async def delete_research(db: AsyncSession, research_id: int):
    # db.query(Research).filter(Research.research_id == research_id).delete()
    await db.execute(db.query(Research).filter(Research.research_id == research_id)).delete()
    await db.commit()
    return {"message": "Research deleted successfully."}