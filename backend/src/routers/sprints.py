from fastapi import APIRouter, File, UploadFile, Depends

from src.database.db import async_session, get_async_session
from src.schemas.filters import PagingFilter
from src.schemas.sprints import SprintOut
from src.services import sprints as service
from src.services.users import get_current_user

router = APIRouter(
    tags=['Спринты'],
    prefix="/sprints",
)


@router.get("/{sprint_id}", response_model=SprintOut | None)
async def get_sprint_info(sprint_id: int, session=Depends(get_async_session)):
    return await service.get_sprint(session=session, sprint_id=sprint_id)


@router.post('/list', response_model=list[SprintOut])
async def get_sprints_list(paging: PagingFilter | None = None, session=Depends(get_async_session)):
    return await service.get_sprints_list(session=session, paging=paging)


@router.post('/import')
async def import_sprints_info(file: UploadFile = File(), current_user=Depends(get_current_user), session=Depends(get_async_session)):
    content = await file.read()
    await service.import_sprints_from_file(session=session, file_content=content, user_id=current_user.id)

