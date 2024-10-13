from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from typing import Optional
from uuid import UUID
import json
from pydantic import ValidationError, HttpUrl

from ...dependencies import get_db, process_image
from ...model import *
from ...auth import get_current_active_lead_researcher
from ...schemas.auth_user import AuthUser
from ...schemas.research_io import ResearchCreate, ResearchUpdate
from ...schemas.research_thumbnail import ResearchThumbnail, RT01
from ...schemas.publication_thumbnail import PublicationThumbnail, PT01

router = APIRouter(
    prefix="/lead_researcher/research",
    tags=["research"],
)

@router.post("/", response_model=ResearchThumbnail)
async def create_research(
    laboratory_id: UUID,
    research: str = Form(...),
    image: UploadFile = File(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    """
    research must come in this form
    {
        "title": "string",
        "body": "string",
        "related_laboratory": {
            "LID": "UUID"
        }
    }
    """
    if image.content_type not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG images are allowed")
    
    try:
        # Manually parse the JSON string
        research_data = json.loads(research)
        # Validate the parsed data against your Pydantic model
        research_object = ResearchCreate.model_validate(research_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in news field")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    processed_images = await process_image(image)
    high_res, low_res = processed_images

    new_research = Research(
        research_id=uuid4(),
        research_name=research_object.title,
        image_high=high_res,
        image_low=low_res,
        body=research_object.body,
        lab_id=laboratory_id
    )

    db.add(new_research)
    db.commit()
    db.refresh(new_research)
    return RT01.to_research_thumbnail(new_research)

@router.patch("/", response_model=ResearchThumbnail)
async def update_research(
    research: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    """ 
    research must come in this form
    {
        "RID": "UUID",
        "title": "string",
        "body": "string",
        "related_laboratory": {
            "LID": "UUID"
        }
    }
    """
    if image is not None and image.content_type not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG images are allowed")
    
    try:
        research_data = json.loads(research)
        research_object = ResearchUpdate.model_validate(research_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in news field")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    processed_images = await process_image(image) if image is not None else (None, None)
    high_res, low_res = processed_images

    updated_research = db.query(Research).filter(Research.research_id == research_object.RID).first()
    if updated_research is None:
        raise HTTPException(status_code=404, detail="Research not found")
    updated_research.research_name = research_object.title
    updated_research.body = research_object.body
    if high_res is not None:
        updated_research.image_high = high_res
    if low_res is not None:
        updated_research.image_low = low_res
    
    db.commit()
    db.refresh(updated_research)
    return RT01.to_research_thumbnail(updated_research)

@router.put("/", response_model=PublicationThumbnail)
def finish_and_migration_to_publication(
    research_id: UUID = Query(...),
    url: HttpUrl = Query(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    research = db.query(Research).filter(Research.research_id == research_id).first()
    if research is None:
        raise HTTPException(status_code=404, detail="Research not found")
    
    new_publication = Publication(
        publication_id=uuid4(),
        publication_name=research.research_name,
        image_high=research.image_high,
        image_low=research.image_low,
        body=research.body,
        url=str(url),
        lab_id=research.lab_id
    )

    db.add(new_publication)

    news_items = db.query(News).filter(News.research_id == research_id).all()
    event_items = db.query(Event).filter(Event.research_id == research_id).all()

    for news in news_items:
        news.research_id = None
        if news.posted:
            news.publication_id = new_publication.publication_id
            db.add(news)
        else:
            db.delete(news)

    for event in event_items:
        event.research_id = None
        if event.posted:
            event.publication_id = new_publication.publication_id
            db.add(event)
        else:
            db.delete(event)

    db.query(person_research).filter(person_research.research_id == research_id).delete()
    db.delete(research)

    db.commit()
    db.refresh(new_publication)
    return PT01.to_publication_thumbnail(new_publication)

@router.delete("/", response_model=ResearchThumbnail)
def delete_research(
    research_id: UUID = Query(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    deleted_research = db.query(Research).filter(Research.research_id == research_id).first()
    if deleted_research is None:
        raise HTTPException(status_code=404, detail="Research not found")
    result = RT01.to_research_thumbnail(deleted_research)
    
    db.delete(deleted_research)
    db.commit()
    return result  