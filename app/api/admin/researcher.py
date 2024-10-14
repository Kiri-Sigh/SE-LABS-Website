from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...model import *
from ...auth import get_current_active_admin
from ...schemas.auth_user import AuthUser
from ...schemas.researcher_thumbnail import ResearcherThumbnail, UT01
from ...schemas.ult.position import Position

router = APIRouter(
    prefix="/admin/researcher",
    tags=["researcher"],
)

@router.patch("/", response_model=ResearcherThumbnail)
def assign_to_be_lead_researcher(
    researcher_id: UUID,
    laboratory_id: UUID,
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_admin)
    ):
    researcher = db.query(Researcher).filter(Researcher.researcher_id == researcher_id).first()
    if researcher is None:
        raise HTTPException(status_code=404, detail="Researcher not found")
    
    researcher.lab_id = laboratory_id

    new_person_lab = person_lab(
        person_id=researcher_id,
        lab_id=laboratory_id,
        role=Position.LeadResearcher
    )

    db.commit()
    db.refresh(researcher)
    return UT01.to_researcher_thumbnail(researcher)

@router.delete("/", response_model=ResearcherThumbnail)
def remove_lead_researcher(
    researcher_id: UUID,
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_admin)
    ):
    researcher = db.query(Researcher).filter(Researcher.researcher_id == researcher_id).first()
    if researcher is None:
        raise HTTPException(status_code=404, detail="Researcher not found")
    
    researcher.lab_id = None

    db.query(person_lab).filter(person_lab.person_id == researcher_id).delete()

    result = UT01.to_researcher_thumbnail(researcher)

    db.commit()
    db.refresh(researcher)
    return result