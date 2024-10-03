from fastapi import APIRouter

from ...schemas.request.researcher.readable import ResearcherLogin as readable

router = APIRouter(
    prefix="/researcher/researcher",
    tags=["researcher"],
)

@router.get("/info/{researcher_id}")
async def get_researcher_info(
    researcher_id: int
        ):
    return {"message": "Researcher info returned"}

@router.post("/login")
async def login(
    body: readable.ResearcherLogin
        ):
    return {"message": "Researcher logged in"}

@router.post("/auto-login")
async def auto_login():
    return {"message": "Researcher auto-logged in"}