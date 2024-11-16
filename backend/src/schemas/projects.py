from pydantic import BaseModel


class ProjectOut(BaseModel):
    id: int
    owner_id: int
    name: str


class ProjectCreate(BaseModel):
    name: str