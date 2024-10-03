from pydantic import BaseModel

from ..unreadable import REU01_research_update as unreadable

class ResearchUpdate(BaseModel):
    Research: unreadable.REU01