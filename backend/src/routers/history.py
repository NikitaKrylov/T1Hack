from fastapi import APIRouter, File, UploadFile, Depends

from fastapi import APIRouter
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

