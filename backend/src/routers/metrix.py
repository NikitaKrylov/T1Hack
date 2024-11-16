from datetime import date

from fastapi import APIRouter, Depends
from src.services import metrics as service
from src.database.db import get_async_session
from fastapi_cache.decorator import cache

router = APIRouter(
    tags=["Метрики"],
    prefix="/metrix",
)

@router.get("")
# @cache(60)
async def get_all_metrix(sprint_id: int, first_date: date, second_date: date,  session=Depends(get_async_session)):
    return await service.get_blockedtasksCHD_metricx(session=session, sprint_id=sprint_id, first_date=first_date, second_date=second_date)
