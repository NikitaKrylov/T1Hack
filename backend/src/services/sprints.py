from io import BytesIO

import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.cruds import base as base_cruds
from src.database.cruds import entities as entities_cruds
from src.database.models import Entity, Sprint
from src.schemas.filters import PagingFilter
from src.schemas.sprints import SprintCreate, SprintOut
from src.services.base import file_to_pandas_dataframe


async def import_sprints_from_file(session: AsyncSession, file_content: bytes, user_id: int) -> None:
    df = file_to_pandas_dataframe(file_content, skip_rows=1)
    normalized_df = await process_sprints(df)

    if normalized_df.empty:
        return

    db_sprints = await get_sprints_list(session)
    db_sprints_df = pd.DataFrame([i.model_dump() for i in db_sprints], columns=list(SprintOut.model_fields.keys()))

    merged = pd.merge(normalized_df, db_sprints_df, how='outer', on='name', indicator=True, suffixes=[None, '__db'])
    to_create_sprints = merged[merged['_merge'] == 'left_only']
    to_create_sprints.drop(columns=['_merge'], inplace=True)
    to_create_sprints.drop(columns=[i for i in to_create_sprints.columns.tolist() if i.endswith('__db')], inplace=True)

    #TODO убрать эту строчку после того как придумаю как избавляться от дупликатов в присвоенных тасках
    if to_create_sprints.empty:
        return

    blank_entities: dict[int, list[int]] = {}

    for row in normalized_df.to_dict('records'):
        sprint_data = SprintCreate(**row)
        sprint_entities = set(row.get('entity_ids', set()))
        db_sprint = await base_cruds.create_one(session=session, model=Sprint, response_model=SprintOut, data=sprint_data, user_id=user_id)
        blank_entities[db_sprint.id] = sprint_entities

    #TODO проверять дупликаты
    for sprint_id, entity_ids in blank_entities.items():
        await entities_cruds.create_blank_entities(session=session, sprint_id=sprint_id, entity_ids=entity_ids)


async def process_sprints(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.rename(columns={
        'sprint_name': 'name',
        'sprint_start_date': 'started_at',
        'sprint_end_date': 'finished_at'
    }, inplace=True)
    df.replace({np.nan: None}, inplace=True)
    df['entity_ids'] = df['entity_ids'].apply(lambda x: [int(i) for i in x[1:-1].split(',')])
    return df


async def create_sprints(session: AsyncSession, sprints: list[SprintCreate]) -> None:
    await base_cruds.create_all(session, model=Sprint, data=sprints)


async def get_sprints_list(session: AsyncSession, paging: PagingFilter | None = None) -> list[SprintOut]:
    return await base_cruds.get_all(session=session, model=Sprint, response_model=SprintOut, paging=paging)


async def get_sprint(session: AsyncSession, sprint_id: int) -> SprintOut | None:
    return await base_cruds.get_one_or_none_by_id(session=session, model=Sprint, response_model=SprintOut, _id=sprint_id)




