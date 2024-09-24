from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class Event(BaseModel):
    EID: str
    title: str
    description: str | None = None
    location: str
    start: datetime
    end: datetime
    laboratory_id: int | None = Field(default=None, gt=0)
    research_id: int | None = Field(default=None, gt=0)

    @field_validator('end')
    def end_date_must_be_after_start_date(cls, v: datetime, info):
        if 'start' in info.data and v <= info.data['start']:
            raise ValueError('end date must be after start date')
        return v

    @field_validator('laboratory_id', 'research_id')
    def ids_must_be_positive(cls, v: int | None):
        if v is not None and v <= 0:
            raise ValueError('laboratory_id and research_id must be positive integers')
        return v