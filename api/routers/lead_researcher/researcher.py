from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session

from ...schemas.request.researcher.readable.ResearcherCreate import ResearcherCreate
from ...dependency.database import get_db
from ...dependency.get_current_user import get_current_user
from ...models.model import Person, UserCredentials, person_lab, person_research
from ...schemas.request.researcher.readable import ResearcherLogin as readable

router = APIRouter(
    prefix="/lead-researcher/researcher",
    tags=["researcher"],
)

@router.post("/")
async def create_researcher_and_assign_to_research(
    body: ResearcherCreate,
    current_user: Person = Depends(get_current_user),
    db: Session = Depends(get_db)
        ):
    researcher = Person(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        role=body.role,
        lab_id=body.lab_id,
        research_id=body.research_id
    )

    db.add(researcher)
    db.commit()
    db.refresh(researcher)

    user_credentials = UserCredentials(
        username=body.username,
        password=body.password
    )

    db.add(user_credentials)
    db.commit()
    db.refresh(user_credentials)

    if body.lab_id:
        user_lab = person_lab(
            person_id=researcher.id,
            lab_id=body.lab_id
        )
        db.add(user_lab)
        db.commit()
        db.refresh(user_lab)
    if body.research_id:
        user_research = person_research(
            person_id=researcher.id,
            research_id=body.research_id
        )
        db.add(user_research)
        db.commit()
        db.refresh(user_research)
    return researcher


@router.patch("/")
async def assign_to_research(
    researcher_id: int,
    research_id: int,
    current_user: Person = Depends(get_current_user),
    db: Session = Depends(get_db)
        ):
    researcher = db.query(Person).filter(Person.id == researcher_id).first()
    researcher.research_id = research_id
    db.commit()
    db.refresh(researcher)
    user_research = person_research(
        person_id=researcher.id,
        research_id=research_id
    )
    db.add(user_research)
    db.commit()
    db.refresh(user_research)
    return researcher

@router.delete("/")
async def delete_researcher_out_of_research(
    researcher_id: int,
    research_id: int,
    current_user: Person = Depends(get_current_user),
    db: Session = Depends(get_db)
        ):
    researcher = db.query(Person).filter(Person.id == researcher_id).first()
    researcher.research_id = None
    db.commit()
    db.refresh(researcher)
    user_research = db.query(person_research).filter(person_research.person_id == researcher_id).first()
    db.delete(user_research)
    db.commit()
    return researcher