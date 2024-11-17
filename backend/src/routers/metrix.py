from datetime import date
from datetime import datetime
from fastapi import APIRouter, Depends, Body
from src.services import metrics as service
from src.database.db import get_async_session
from fastapi_cache.decorator import cache

router = APIRouter(
    tags=["Метрики"],
    prefix="/metrix",
)

@router.post("")
# @cache(60)
async def get_all_metrix(sprint_id: int = Body(), first_date: date = Body(), second_date: date = Body(),  session=Depends(get_async_session)):
    start = datetime.now()
    result = await service.get_sprint_metrics(session=session, sprint_id=sprint_id, first_date=first_date, second_date=second_date)
    end = datetime.now()
    print(f'All time: {end - start}')
    return result

