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
    name: str | None = None
    area: str | None = None
    type: str | None = None
    status: str | None = None
    state: str | None = None
    priority: str | None = None
    ticket_number: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    parent_ticket_id: int | None = None
    due_date: date | None = None
    rank: str | None = None
    estimation: int | None = None
    workgroup: str | None = None
    resolution: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    assignee: str | None = None
    owner: str | None = None


class EntityUpdate(EntityOut):
    pass


class EntityCreate(BaseModel):
    entity_id: int
    sprint_id: int
    name: str | None = None
    area: str | None = None
    type: str | None = None
    status: str | None = None
    state: str | None = None
    priority: str | None = None
    ticket_number: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    parent_ticket_id: int | None = None
    due_date: date | None = None
    rank: str | None = None
    estimation: int | None = None
    workgroup: str | None = None
    resolution: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    assignee: str | None = None
    owner: str | None = None


class EntityWithHistoryChangesOut(EntityOut):
    # changes_history: list[EntityOut]
    pass

