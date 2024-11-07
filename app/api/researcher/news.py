from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from uuid import UUID, uuid4
from datetime import datetime
import json
from pydantic import ValidationError

from ...dependencies import get_db, process_image
from ...auth import get_current_active_researcher
from ...model import *
from ...schemas.auth_user import AuthUser
from ...schemas.news_io import NewsCreate
from ...schemas.news_thumbnail import NewsThumbnail, NT01

router = APIRouter(
    prefix="/researcher/news",
    tags=["news"],
)

@router.post("/", response_model=NewsThumbnail)
async def create_news(
    research_id: UUID,
    news: str = Form(...),
    image: UploadFile = File(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_researcher)
):
    """
    news must come in this form
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
    
    try:
        # Manually parse the JSON string
        news_data = json.loads(news)
        # Validate the parsed data against your Pydantic model
        news_object = NewsCreate.model_validate(news_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in news field")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    processed_images = await process_image(image)
    high_res, low_res = processed_images
    
    new_news = News(
        news_id=uuid4(),
        news_name=news_object.title,
        image_high=high_res,
        image_low=low_res,
        body=news_object.body,
        date=datetime.now(),
        posted=False,
        lab_id=news_object.related_laboratory.LID,
        research_id=research_id
    )
    
    db.add(new_news)
    db.commit()
    db.refresh(new_news)
    return NT01.to_news_thumbnail(new_news)
