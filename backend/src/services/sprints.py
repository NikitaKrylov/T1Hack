from io import BytesIO

import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.cruds import base as base_cruds
from src.database.cruds import sprints as sprints_cruds
from src.database.cruds import entities as entities_cruds
from src.database.models import Entity, Sprint
from src.schemas.entities import EntityCreate
from src.schemas.sprints import SprintCreate, SprintOut
from src.services.base import file_to_pandas_dataframe


async def import_sprints_from_file(session: AsyncSession, file_content: bytes) -> None:
    df = file_to_pandas_dataframe(file_content, skip_rows=1)
    normalized_df = await process_sprints(df)

    blank_entities: dict[int, list[int]] = {}

    for row in normalized_df.to_dict('records'):
        sprint_data = SprintCreate(**row)
        sprint_entities = row.get('entity_ids', [])
        db_sprint = await base_cruds.create_one(session=session, model=Sprint, response_model=SprintOut, data=sprint_data)
        blank_entities[db_sprint.id] = sprint_entities

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
    return df


async def create_sprints(session: AsyncSession, sprints: list[SprintCreate]) -> None:
    await base_cruds.create_all(session, model=Sprint, data=sprints)




