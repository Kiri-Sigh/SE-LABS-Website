from sqlalchemy.orm import Session

from ..models.model import Laboratory
from ..schemas.core.laboratory import LaboratoryCreate, LaboratoryDB

def create_laboratory(db: Session, laboratory_create: LaboratoryCreate) -> LaboratoryDB:
    # Create a new laboratory instance
    new_laboratory = Laboratory(
        **laboratory_create.model_dump()
    )

    # Add the new laboratory to the database
    db.add(new_laboratory)
    db.commit()

    # Refresh the new laboratory to ensure it reflects the current state in the database
    db.refresh(new_laboratory)

    return new_laboratory

def get_laboratory(db: Session, laboratory_id: int) -> LaboratoryDB:
    # Fetch the laboratory from the database
    laboratory = db.query(Laboratory).filter(Laboratory.laboratory_id == laboratory_id).first()
    if not laboratory:
        raise ValueError("Laboratory not found")

    return laboratory

def get_laboratories(db: Session, skip: int = 0, limit: int = 100) -> list[LaboratoryDB]:
    # Fetch all laboratories from the database
    laboratories = db.query(Laboratory).offset(skip).limit(limit).all()

    return laboratories

def update_laboratory(db: Session, laboratory_id: int, laboratory_update: LaboratoryCreate) -> LaboratoryDB:
    # Fetch the laboratory to be updated
    laboratory = db.query(Laboratory).filter(Laboratory.laboratory_id == laboratory_id).first()
    if not laboratory:
        raise ValueError("Laboratory not found")

    # Update the laboratory with the new data
    for key, value in laboratory_update.dict().items():
        setattr(laboratory, key, value)

    # Commit the changes
    db.commit()

    # Refresh the laboratory to ensure it reflects the current state in the database
    db.refresh(laboratory)

    return laboratory

def delete_laboratory(db: Session, laboratory_id: int) -> LaboratoryDB:
    # Fetch the laboratory to be deleted
    laboratory = db.query(Laboratory).filter(Laboratory.laboratory_id == laboratory_id).first()
    if not laboratory:
        raise ValueError("Laboratory not found")

    # Delete the laboratory from the database
    db.delete(laboratory)
    db.commit()

    return laboratory