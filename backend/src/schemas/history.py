from pydantic import BaseModel
from datetime import date, datetime


class HistoryOut(BaseModel):
    id: int
    entity_id: int
    property_name: str | None
    date: datetime | None
    version: int | None
    change_type: str | None
    history_change: str | None


class HistoryCreate(BaseModel):
    entity_id: int
    property_name: str | None
    date: datetime | None
    version: int | None
    change_type: str | None
    history_change: str | None