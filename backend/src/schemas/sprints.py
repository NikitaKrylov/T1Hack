from datetime import datetime

from pydantic import BaseModel


class SprintOut(BaseModel):
    id: int
    name: str
    sprint_status: str
    created_at: datetime
    started_at: datetime
    finished_at: datetime
    # entities: list[int]


class SprintCreate(BaseModel):
    name: str
    sprint_status: str
    started_at: datetime
    finished_at: datetime
    # entities: list[int]