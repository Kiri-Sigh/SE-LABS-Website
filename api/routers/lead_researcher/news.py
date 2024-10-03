from fastapi import APIRouter, Header

router = APIRouter(
    prefix="/lead-researcher/news",
    tags=["news"],
)

@router.get("/commit")
async def get_commit(
    laboratory_id: int,
    token: str = Header()
        ):
    return {"message": "News committed"}

@router.patch("/")
async def update_news(
    news_id: int,
    approve: bool,
    token: str = Header()
        ):
    return {"message": "News updated"}

@router.delete("/")
async def delete_news(
    news_id: int,
    token: str = Header()
        ):
    return {"message": "News deleted"}