from fastapi import APIRouter, File, UploadFile, Depends
from src.schemas.filters import PagingFilter, EntityHistoryFilter
from src.schemas.history import HistoryOut
from src.services import history as service
from src.database.db import get_async_session

router = APIRouter(
    tags=['История изменений'],
    prefix='/history'
)


@router.post('/import')
async def import_entity_histories(file: UploadFile = File(), session=Depends(get_async_session)):
    content = await file.read()
    await service.import_history_data(session=session, file_content=content)


@router.post('/list', response_model=list[HistoryOut])
async def get_entity_history_list(filters: EntityHistoryFilter | None = None, paging: PagingFilter | None = None, session=Depends(get_async_session)):
    return await service.get_entity_histories(session=session, paging=paging, filters=filters)

