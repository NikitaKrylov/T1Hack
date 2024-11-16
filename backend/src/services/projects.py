from sqlalchemy.ext.asyncio import AsyncSession
from src.database.cruds import base as base_cruds
from src.database.models import Project
from src.schemas.filters import PagingFilter
from src.schemas.projects import ProjectCreate, ProjectOut


async def create_project(session: AsyncSession, user_id: int, project: ProjectCreate) -> ProjectOut:
    return await base_cruds.create_one(session=session, model=Project, response_model=ProjectOut, data=project, owner_id=user_id)


async def get_users_projects_list(session: AsyncSession, user_id: int, paging: PagingFilter | None = None) -> list[ProjectOut]:
    return await base_cruds.get_all(session=session, model=Project, response_model=ProjectOut, paging=paging)





