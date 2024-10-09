from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session

from ...dependency.database import get_db
from ...models.model import Person
from ...schemas.response.researcher.UT01_researcher_thumbnail import RT01
from ...schemas.response.researcher.UIMG01_researcher_image import UIMG01

router = APIRouter(
    prefix="/user/researcher",
    tags=["researcher"],
)

@router.get("/thumbnail", response_model_by_alias=list[RT01])
async def get_researcher_thumbnail(
        laboratory_id: Optional[str] = None,
        research_id: Optional[str] = None,
        amount: Optional[int] = 0,
        page: Optional[int] = 1,
        db: Session = Depends(get_db)
        ):
    researcher = db.query(Person)
    if laboratory_id:
        researcher = researcher.filter(Person.lab_id == laboratory_id)
    if research_id:
        researcher = researcher.filter(Person.research_id == research_id)
    offset = (page - 1) * amount
    researcher = researcher.offset(offset).limit(amount).all()
    return [RT01(researcher) for researcher in researcher]

@router.get("/image-high", response_model=UIMG01)
async def get_researcher_image_high(
        researcher_id: str,
        db: Session = Depends(get_db)
        ):
    researcher = db.query(Person).filter(Person.id == researcher_id).first()
    return UIMG01(researcher)

@router.get("/image-low", response_model=UIMG01)
async def get_researcher_image_low(
        researcher_id: str,
        db: Session = Depends(get_db)
        ):
    researcher = db.query(Person).filter(Person.id == researcher_id).first()
    return UIMG01(researcher)