from fastapi import APIRouter, Depends

from src.database.db import get_async_session
from src.schemas.filters import PagingFilter
from src.schemas.projects import ProjectOut, ProjectCreate
from src.schemas.users import UserOut
from src.services import projects as service
from src.services.users import get_current_user

router = APIRouter(
    tags=['Проекты'],
    prefix="/projects",
)


@router.post('', response_model=ProjectOut)
async def create_project(data: ProjectCreate, current_user: UserOut = Depends(get_current_user), session=Depends(get_async_session)):
    return await service.create_project(session=session, project=data, user_id=current_user.id)


@router.post('/list', response_model=list[ProjectOut])
async def get_projects_list(paging: PagingFilter, current_user: UserOut = Depends(get_current_user), session=Depends(get_async_session)):
    return await service.get_users_projects_list(session=session, paging=paging, user_id=current_user.id)

