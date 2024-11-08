from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from uuid import UUID, uuid4
from datetime import datetime
import json
from pydantic import ValidationError
from typing import Optional
from ...schemas.ult.position import Position

from ...dependencies import get_db, process_image
from ...auth import get_current_active_authorized_user
from ...model import *
from ...schemas.auth_user import AuthUser
from ...schemas.news_io import NewsCreate
from ...schemas.news_thumbnail import NewsThumbnail, NT01
from ...crud.news import create_news

router = APIRouter(
    prefix="/researcher/news",
    tags=["news"],
)

@router.post("/", response_model=NewsThumbnail)
async def create_news_API(
    research_id: Optional[UUID] = Query(None),
    laboratory_id: Optional[UUID] = Query(None),
    news: str = Form(...),
    image: UploadFile = File(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_authorized_user)
):
    """
    news must come in this form \n
    {
        "title": str,
        "body": str,
        "related_laboratory": {
            "LID": UUID,
            "related_research": {
                "RID": UUID
            }
        }
    }
    """
    if image.content_type not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG images are allowed")
    
    news_data = None
    news_object: NewsCreate = None
    
    try:
        news_data = json.loads(news)
        news_object = NewsCreate.model_validate(news_data)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON in event field: " + str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {str(e)}")

    new_news = await create_news(
        db=db,
        news=news_object,
        image=image,
        laboratory_id=laboratory_id,
        research_id=research_id
    )

    return NT01.to_news_thumbnail(new_news)