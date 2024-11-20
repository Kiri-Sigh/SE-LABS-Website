from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from typing import Optional
from uuid import UUID
import json
from pydantic import ValidationError

from dependencies import get_db, process_image
from model import *
from auth import get_current_active_lead_researcher
from schemas.auth_user import AuthUser
from schemas.publication_io import PublicationUpdate
from schemas.publication_thumbnail import PublicationThumbnail, PT01

router = APIRouter(
    prefix="/lead_researcher/publication",
    tags=["publication"],
)

@router.patch("/", response_model=PublicationThumbnail)
async def update_publication(
    publication: str,
    image: Optional[UploadFile] = File(None),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    """
    publication must come in this form
    {
        "PID": "UUID",
        "title": "string",
        "body": "string",
        "link": "URL"
    }
    """
    if image is not None and image.content_type not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG images are allowed")
    
    try:
        publication_data = json.loads(publication)
        publication_object = PublicationUpdate.model_validate(publication_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in news field")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    processed_images = await process_image(image) if image is not None else (None, None)
    high_res, low_res = processed_images

    updated_publication = db.query(Publication).filter(Publication.publication_id == publication_object.PID).first()
    if updated_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    updated_publication.publication_name = publication_object.title
    updated_publication.body = publication_object.body
    updated_publication.url = str(publication_object.link)
    if high_res is not None:
        updated_publication.image_high = high_res
    if low_res is not None:
        updated_publication.image_low = low_res
    
    db.commit()
    db.refresh(updated_publication)
    return PT01.to_publication_thumbnail(updated_publication)

@router.delete("/")
def delete_publication(
    publication_id: UUID = Query(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    publication = db.query(Publication).filter(Publication.publication_id == publication_id).first()
    if publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    
    db.delete(publication)
    db.commit()
    return PT01.to_publication_thumbnail(publication)