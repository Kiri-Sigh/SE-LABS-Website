from pydantic import BaseModel

from ..laboratory.LT01_laboratory_thumbnail import LT01
from ..research.RT01_research_thumbnail import RT01

class UT01(BaseModel):
    uid: str
    name: str
    mail: str
    position: str
    related_laboratory: list[LT01]
    related_research: list[RT01]