from fastapi import APIRouter, Header, Depends

from ...schemas.request.research.readable import ResearchCreate, ResearchUpdate
from ...schemas.request.publication.readable import PublicationTranform
from ...dependency.get_current_user import get_current_user
from ...dependency.database import get_db
from ...models.model import Research, Publication, News, Event

router = APIRouter(
    prefix="/lead-researcher/research",
    tags=["research"],
)

@router.post("/")
async def create_research(
    body: ResearchCreate.ResearchCreate,
    current_user: Research = Depends(get_current_user),
    db = Depends(get_db)
        ):
    research = Research(
        title=body.title,
        body=body.body,
        lab_id=body.lab_id,
        image_high=body.image_high,
        image_low=body.image_low
    )
    db.add(research)
    db.commit()
    db.refresh(research)
    return research

@router.patch("/")
async def update_research(
    body: ResearchUpdate.ResearchUpdate,
    current_user: Research = Depends(get_current_user),
    db = Depends(get_db)
        ):
    research = db.query(Research).filter(Research.id == body.research_id).first()
    research.title = body.title
    research.body = body.body
    research.lab_id = body.lab_id
    research.image_high = body.image_high
    research.image_low = body.image_low
    db.commit()
    db.refresh(research)
    return research

@router.put("/")
async def finish_research(
    research_id: int,
    body: PublicationTranform.PublicationTranform,
    current_user: Research = Depends(get_current_user),
    db = Depends(get_db)
        ):
    research = db.query(Research).filter(Research.id == research_id).first()
    publication = Publication(
        title=research.title,
        body=research.body,
        lab_id=research.lab_id,
        image_high=research.image_high,
        image_low=research.image_low
    )
    db.add(publication)
    db.commit()
    db.refresh(publication)

    db.query(News).filter(News.research_id == research_id).update(
        {"research_id": None, "publication_id": publication.id}
    )
    db.query(Event).filter(Event.research_id == research_id).update(
        {"research_id": None, "publication_id": publication.id}
    )
    db.delete(research)
    db.commit()
    db.refresh(publication)
    return publication

@router.delete("/")
async def delete_research(
    research_id: int,
    current_user: Research = Depends(get_current_user),
    db = Depends(get_db)
        ):
    research = db.query(Research).filter(Research.id == research_id).first()
    db.delete(research)
    db.commit()
    return research