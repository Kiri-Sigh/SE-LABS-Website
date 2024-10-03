from pydantic import BaseModel

from ..unreadable import REC01_research_create as unreadable

class ResearchCreate(BaseModel):
    Research: unreadable.REC01