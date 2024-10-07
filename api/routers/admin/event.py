from fastapi import APIRouter, Depends, Header

router = APIRouter(
    prefix="/admin/event",
    tags=["event"],
)