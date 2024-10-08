from fastapi import APIRouter, Header

from ...schemas.request.researcher.readable import ResearcherLogin as readable

router = APIRouter(
    prefix="/researcher/researcher",
    tags=["researcher"],
)

@router.get("/info/{researcher_id}")
async def get_researcher_info(
    researcher_id: int,
    token: str = Header()
        ):
    return {"message": "Researcher info returned"}

@router.post("/login")
async def login(
    body: readable.ResearcherLogin,
    token: str = Header()
        ):
    return {"message": "Researcher logged in"}

@router.post("/auto-login")
async def auto_login(
    token: str = Header()
        ):
    return {"message": "Researcher auto-logged in"}