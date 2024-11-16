import numpy as np
import pandas as pd
from src.schemas.filters import PagingFilter
from src.services.base import file_to_pandas_dataframe
from src.database.cruds import base as base_cruds
from src.database.cruds import entities as entities_cruds
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Entity
from src.schemas.entities import EntityOut, EntityCreate, EntityUpdate


async def process_entities(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.drop_duplicates(ignore_index=True, inplace=True)
    df['entity_id'] = df['entity_id'].astype(int)
    df['parent_ticket_id'] = df['parent_ticket_id'].astype(int, errors='ignore')
    df['due_date'] = pd.to_datetime(df['due_date'], format='%m/%d/%y').dt.date
    df.replace({np.nan: None}, inplace=True)
    df.rename(columns={
        'create_date': 'created_at',
        'update_date': 'updated_at',
    }, inplace=True)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S.%f')
    return df


async def import_entities(session: AsyncSession, file_content: bytes) -> None:
    new_df = file_to_pandas_dataframe(file_content, skip_rows=1)
    normalized_df = await process_entities(new_df)

    db_entities = await get_entities_list(session)
    db_df = pd.DataFrame([i.model_dump() for i in db_entities], columns=list(EntityOut.model_fields.keys()))

    merged = pd.merge(normalized_df, db_df, on=['entity_id'], indicator=True, how='outer', suffixes=[None, '__db'])
    to_update_entities = merged[merged['_merge'] == 'both']
    to_update_entities.drop(columns=['_merge',], inplace=True)
    to_update_entities.drop(columns=[i for i in to_update_entities.columns.tolist() if i.endswith('__db')], inplace=True)

    await entities_cruds.update_entities_by_ids(session=session, entities=[EntityUpdate(**i) for i in to_update_entities.to_dict(orient='records')])


async def get_entities_list(session: AsyncSession, paging: PagingFilter | None = None) -> list[EntityOut]:
    return await base_cruds.get_all(session=session, model=Entity, response_model=EntityOut, paging=paging)

