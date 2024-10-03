from fastapi import APIRouter

router = APIRouter(
    prefix="/lead-researcher/news",
    tags=["news"],
)

@router.get("/commit")
async def get_commit(
    laboratory_id: int
        ):
    return {"message": "News committed"}

@router.patch("/")
async def update_news(
    news_id: int,
    approve: bool
        ):
    return {"message": "News updated"}

@router.delete("/")
async def delete_news(
    news_id: int
        ):
    return {"message": "News deleted"}