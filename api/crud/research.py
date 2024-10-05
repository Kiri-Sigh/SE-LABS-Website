from sqlalchemy.orm import Session
from ..models.model import Research
from ..schemas.core.research import ResearchCreate, ResearchDB

def get_research(db: Session, research_id: int) -> ResearchDB:
    return db.query(Research).filter(Research.research_id == research_id).first()

def get_research_list(db: Session, skip: int = 0, limit: int = 100) -> list[ResearchDB]:
    return db.query(Research).offset(skip).limit(limit).all()

def create_research(db: Session, research: ResearchCreate) -> ResearchDB:
    db_research = Research(**research.model_dump())
    db.add(db_research)
    db.commit()
    db.refresh(db_research)
    return db_research

def edit_research(db: Session, research_id: int, research: ResearchCreate) -> ResearchDB:
    db_research = db.query(Research).filter(Research.research_id == research_id).first()
    if not db_research:
        return None
    for key, value in research.model_dump().items():
        if value is not None:
            setattr(db_research, key, value)
    db.commit()
    db.refresh(db_research)
    return db_research

def delete_research(db: Session, research_id: int):
    db.query(Research).filter(Research.research_id == research_id).delete()
    db.commit()
    return {"message": "Research deleted successfully."}