from fastapi import APIRouter

from ...schemas.request.researcher.readable import ResearcherCreate as readable

router = APIRouter(
    prefix="/lead-researcher/researcher",
    tags=["researcher"],
)

@router.post("/")
async def create_researcher_and_assign_to_research(
    body: readable.ResearcherCreate
        ):
    return {"message": "Researcher created"}

@router.patch("/")
async def assign_to_research(
    researcher_id: int,
    research_id: int
        ):
    return {"message": "Researcher updated"}

@router.delete("/")
async def delete_researcher_out_of_research(
    researcher_id: int,
    research_id: int
        ):
    return {"message": "Researcher deleted"}