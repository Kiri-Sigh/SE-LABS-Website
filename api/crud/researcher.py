from sqlalchemy.orm import Session

from ..models.model import Researcher
from ..schemas.core.researcher import ResearcherCreate, ResearcherDB

def create_researcher(db: Session, researcher_create: ResearcherCreate) -> ResearcherDB:
    # Create a new researcher instance
    new_researcher = Researcher(
        **researcher_create.model_dump()
    )

    # Add the new researcher to the database
    db.add(new_researcher)
    db.commit()

    # Refresh the new researcher to ensure it reflects the current state in the database
    db.refresh(new_researcher)

    return new_researcher

def get_researcher(db: Session, researcher_id: int) -> ResearcherDB:
    # Fetch the researcher from the database
    researcher = db.query(Researcher).filter(Researcher.researcher_id == researcher_id).first()
    if not researcher:
        raise ValueError("Researcher not found")

    return researcher

def get_researchers(db: Session, skip: int = 0, limit: int = 100) -> list[ResearcherDB]:
    # Fetch all researchers from the database
    researchers = db.query(Researcher).offset(skip).limit(limit).all()

    return researchers

def update_researcher(db: Session, researcher_id: int, researcher_update: ResearcherCreate) -> ResearcherDB:
    # Fetch the researcher to be updated
    researcher = db.query(Researcher).filter(Researcher.researcher_id == researcher_id).first()
    if not researcher:
        raise ValueError("Researcher not found")

    # Update the researcher with the new data
    for key, value in researcher_update.dict().items():
        setattr(researcher, key, value)

    # Commit the changes
    db.commit()

    # Refresh the researcher to ensure it reflects the current state in the database
    db.refresh(researcher)

    return researcher

def delete_researcher(db: Session, researcher_id: int) -> ResearcherDB:
    # Fetch the researcher to be deleted
    researcher = db.query(Researcher).filter(Researcher.researcher_id == researcher_id).first()
    if not researcher:
        raise ValueError("Researcher not found")

    # Delete the researcher from the database
    db.delete(researcher)
    db.commit()

    return researcher