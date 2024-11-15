from datetime import date, datetime

from pydantic import BaseModel


class EntityChangeOut(BaseModel):
    id: int
    entity_id: int
    # entity: str
    property_name: str | None
    date: datetime | None
    version: int | None
    change_type: str | None
    changed_from: str | None
    changed_to: str | None


class EntityChangeCreate(BaseModel):
    entity_id: int
    property_name: str | None
    date: datetime | None
    version: int | None
    change_type: str | None
    changed_from: str | None
    changed_to: str | None


class EntityOut(BaseModel):
    id: int
    entity_id: int
    sprint_id: int
    name: str
    area: str
    type: str
    status: str
    state: str
    priority: str
    ticket_number: str
    created_at: str
    updated_at: str
    parent_ticket_id: int | None
    due_date: date | None
    rank: str
    estimation: int | None
    workgroup: str | None
    resolution: str | None


class EntityCreate(BaseModel):
    entity_id: int
    sprint_id: int | None = None
    name: str
    area: str
    type: str
    status: str
    state: str
    priority: str
    ticket_number: str
    created_at: datetime
    updated_at: datetime
    parent_ticket_id: int | None
    due_date: date | None
    rank: str
    estimation: int | None
    workgroup: str | None
    resolution: str | None


class EntityWithHistoryChangesOut(EntityOut):
    changes_history: list[EntityOut]

