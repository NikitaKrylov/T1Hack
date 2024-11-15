from fastapi import APIRouter, File, UploadFile, Depends

from src.database.db import async_session, get_async_session
from src.services import sprints as service

router = APIRouter(
    tags=['Спринты'],
    prefix="/sprints",
)


@router.post('/import')
async def import_sprints_info(file: UploadFile = File(), session=Depends(get_async_session)):
    content = await file.read()
    await service.import_sprints_from_file(session, content)


@router.post('/entities/import')
async def import_sprint_entities(file: UploadFile = File(), session=Depends(get_async_session)):
    content = await file.read()
    await service.import_entities_from_file(session=session, file_content=content)


@router.post('/history/changes/import')
async def import_sprint_entities_history_changes(file: UploadFile = File()):
    content = await file.read()
