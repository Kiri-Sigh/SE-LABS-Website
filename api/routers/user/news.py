from fastapi import APIRouter, HTTPException
from ...pydantic.news import News
from ...fake_db.news import fake_db_news

router = APIRouter(
    prefix="/user/news",
    tags=["news"],
)

@router.get("/thumbnail", response_model=list[News])
def get_thumbnail(amount: int, laboratory_id: int | None = None, research_id: int | None = None):
    if amount < 0:
        raise HTTPException(status_code=400, detail="Amount must be a positive integer")
    if amount > len(fake_db_news):
        raise HTTPException(status_code=400, detail="Amount exceeds the number of events in the database")

    filtered_events = fake_db_news
    if laboratory_id is not None:
        filtered_events = [event for event in filtered_events if event["laboratory_id"] == laboratory_id]
    if research_id is not None:
        filtered_events = [event for event in filtered_events if event["research_id"] == research_id]

    return filtered_events[:amount]