from fastapi import APIRouter, Header

from ...schemas.request.research.readable import ResearchCreate, ResearchUpdate
from ...schemas.request.publication.readable import PublicationTranform

router = APIRouter(
    prefix="/lead-researcher/research",
    tags=["research"],
)

@router.post("/")
async def create_research(
    body: ResearchCreate.ResearchCreate,
    token: str = Header()
        ):
    return {"message": "Research posted"}

@router.patch("/")
async def update_research(
    body: ResearchUpdate.ResearchUpdate,
    token: str = Header()
        ):
    return {"message": "Research updated"}

@router.put("/")
async def finish_research(
    research_id: int,
    body: PublicationTranform.PublicationTranform,
    token: str = Header()
        ):
    return {"message": "Research finished"}

@router.delete("/")
async def delete_research(
    research_id: int,
    token: str = Header()
        ):
    return {"message": "Research deleted"}