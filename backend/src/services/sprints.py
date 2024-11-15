from io import BytesIO

import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.cruds import base as crud
from src.database.models import Entity
from src.schemas.entities import EntityCreate
from src.schemas.sprints import SprintCreate


def file_to_pandas_dataframe(file_content: bytes, skip_rows: int = 0):
    io = BytesIO(file_content)
    return pd.read_csv(io, skip_blank_lines=True, skiprows=skip_rows, sep=';')


async def import_sprints_from_file(session: AsyncSession, file_content: bytes) -> None:
    df = file_to_pandas_dataframe(file_content, skip_rows=1)
    data = [SprintCreate(**i) for i in df.to_dict('records')]
    await create_sprints(session, data)


async def process_sprints(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # df.drop_duplicates(ignore_index=True)
    # df['entity_id'] = df['entity_id'].astype('str')
    # df['parent_ticket_id'] = df['parent_ticket_id'].astype('str').apply(lambda x: x[:-2])


async def process_entities(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.drop_duplicates(ignore_index=True, inplace=True)
    df['entity_id'] = df['entity_id'].astype('str')
    df['parent_ticket_id'] = df['parent_ticket_id'].astype(int, errors='ignore')
    df['due_date'] = pd.to_datetime(df['due_date'], format='%m/%d/%y').dt.date
    df.replace({np.nan: None}, inplace=True)
    df.rename(columns={
        'create_date': 'created_at',
        'update_date': 'updated_at',
    }, inplace=True)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S.%f')
    # df['created_at'] = df['created_at'].apply(lambda x: x.to_pydatetime())
    return df


async def import_entities_from_file(session: AsyncSession, file_content: bytes) -> None:
    df = file_to_pandas_dataframe(file_content, skip_rows=1)
    normalized_df = await process_entities(df)
    new_entities = [EntityCreate(**i) for i in normalized_df.to_dict('records')]
    await create_entities(session, new_entities)


async def create_sprints(session: AsyncSession, sprints: list[SprintCreate]) -> None:
    await crud.create_all(session, model=SprintCreate, data=sprints)


async def create_entities(session: AsyncSession, entities: list[EntityCreate]) -> None:
    await crud.create_all(session, model=Entity, data=entities)



