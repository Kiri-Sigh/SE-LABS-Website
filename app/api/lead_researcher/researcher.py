from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from typing import Optional
from uuid import UUID
import json
from pydantic import ValidationError
from passlib.context import CryptContext

from ...dependencies import get_db, process_image
from ...model import *
from ...auth import get_current_active_lead_researcher
from ...schemas.auth_user import AuthUser
from ...schemas.researcher_io import ResearcherCreate
from ...schemas.researcher_thumbnail import ResearcherThumbnail, UT01

# Set up the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/lead_researcher/researcher",
    tags=["researcher"],
)

@router.post("/")
async def create_user(
    researcher: str,
    image: UploadFile,
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    """
    researcher must come in this form
    {
        "password": "string",
        "name": "string",
        "mail": "string"
    }
    """
    if image is not None and image.content_type not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG images are allowed")
    
    try:
        researcher_data = json.loads(researcher)
        researcher_object = ResearcherCreate.model_validate(researcher_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in news field")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    processed_images = await process_image(image) if image is not None else (None, None)
    high_res, low_res = processed_images

    new_researcher = Researcher(
        user_id=uuid4(),
        full_name=researcher_object.name,
        image_high=high_res,
        image_low=low_res,
        gmail=researcher_object.mail,
        highest_role=Position.Free,
        admin=False,
        active=True
    )

    db.add(new_researcher)
    db.commit()

    new_user_credentials = UserCredentials(
        user_id=new_researcher.user_id,
        password_hash=pwd_context.hash(researcher_object.password)
    )

    db.add(new_user_credentials)
    db.commit()

    db.refresh(new_researcher)
    db.refresh(new_user_credentials)

    return UT01.to_researcher_thumbnail(new_researcher)

@router.patch("/", response_model=ResearcherThumbnail)
def assign_researcher_to_research(
    researcher_id: UUID = Query(...),
    research_id: UUID = Query(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    researcher = db.query(Researcher).filter(Researcher.user_id == researcher_id).first()
    if researcher is None:
        raise HTTPException(status_code=404, detail="Researcher not found")
    
    research = db.query(Research).filter(Research.research_id == research_id).first()
    if research is None:
        raise HTTPException(status_code=404, detail="Research not found")
    
    new_person_research = person_research(
        user_id=researcher_id,
        research_id=research_id,
        role=Position.Researcher
    )
    
    # check the highest role of the researcher and update it if necessary
    if researcher.highest_role == Position.Free:
        researcher.highest_role = Position.Researcher

    db.add(new_person_research)
    db.commit()
    db.refresh(researcher)
    return UT01.to_researcher_thumbnail(researcher)

@router.delete("/", response_model=ResearcherThumbnail)
def kick_from_research(
    researcher_id: UUID = Query(...),
    research_id: UUID = Query(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    researcher = db.query(Researcher).filter(Researcher.user_id == researcher_id).first()
    if researcher is None:
        raise HTTPException(status_code=404, detail="Researcher not found")
    
    research = db.query(Research).filter(Research.research_id == research_id).first()
    if research is None:
        raise HTTPException(status_code=404, detail="Research not found")
    
    existe_person_research = db.query(person_research).filter(
        person_research.user_id == researcher_id,
        person_research.research_id == research_id
    ).first()
    if existe_person_research is None:
        raise HTTPException(status_code=404, detail="Researcher not assigned to research")
    
    if len(researcher.researches) == 0:
        researcher.highest_role = Position.Free
    
    db.delete(existe_person_research)
    db.commit()
    db.refresh(researcher)
    return UT01.to_researcher_thumbnail(researcher)