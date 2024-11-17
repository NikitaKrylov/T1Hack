from fastapi import APIRouter, File, UploadFile, Depends
from fastapi import APIRouter
from src.schemas.entities import EntityOut
from src.schemas.filters import PagingFilter
from src.services import entities as service
from src.database.db import get_async_session

router = APIRouter(
    tags=['Задачи'],
    prefix='/entities'
)


@router.post('/import')
async def import_entities(file: UploadFile = File(), session=Depends(get_async_session)):
    content = await file.read()
    await service.import_entities(session=session, file_content=content)


@router.post('/list', response_model=list[EntityOut])
async def get_entities_list(paging: PagingFilter | None = None, session=Depends(get_async_session)):
    return await service.get_entities_list(session=session, paging=paging)
