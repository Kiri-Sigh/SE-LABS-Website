from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session

from ...schemas.request.researcher.readable import ResearcherCreate as readable
from ...dependency.database import get_db
from ...dependency.get_current_user import get_current_user
from ...models.model import Person, UserCredentials, person_lab, person_research
from ...schemas.request.researcher.readable import ResearcherLogin as readable

router = APIRouter(
    prefix="/admin/researcher",
    tags=["researcher"],
)

@router.patch("/")
async def assign_to_lead_researcher(
    laboratory_id: int,
    researcher_id: int,
    current_user: Person = Depends(get_current_user),
    db: Session = Depends(get_db)
        ):
    researcher = db.query(Person).filter(Person.id == researcher_id).first()
    researcher.lab_id = laboratory_id
    db.commit()
    db.refresh(researcher)
    person_lab = db.query(person_lab).filter(person_lab.person_id == researcher_id).first()
    person_lab.lab_id = laboratory_id
    db.commit()
    db.refresh(person_lab)
    return researcher



@router.delete("/")
async def delete_researcher_out_of_laboratory(
    laboratory_id: int,
    researcher_id: int,
    current_user: Person = Depends(get_current_user),
    db: Session = Depends(get_db)
        ):
    researcher = db.query(Person).filter(Person.id == researcher_id).first()
    researcher.lab_id = None
    db.commit()
    db.refresh(researcher)
    person_lab = db.query(person_lab).filter(person_lab.person_id == researcher_id).first()
    person_lab.lab_id = None
    db.commit()
    db.refresh(person_lab)
    return researcher
