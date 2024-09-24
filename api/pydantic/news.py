from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class News(BaseModel):
    NID: str
    title: str
    body: str
    date: datetime
    laboratory_id: int | None = Field(default=None, gt=0)
    research_id: int | None = Field(default=None, gt=0)

    @field_validator('laboratory_id', 'research_id')
    def ids_must_be_positive(cls, v: int | None):
        if v is not None and v <= 0:
            raise ValueError('laboratory_id and research_id must be positive integers')
        return v