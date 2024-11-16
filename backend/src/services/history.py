import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from src.database.cruds import base as base_cruds
from src.database.models import EntityChanging
from src.schemas.filters import PagingFilter
from src.schemas.history import HistoryOut, HistoryCreate
from src.services.base import file_to_pandas_dataframe


async def import_history_data(session: AsyncSession, file_content: bytes) -> None:
    df = file_to_pandas_dataframe(file_content, skip_rows=1)
    normalized_df = await process_history(df)
    to_create_history_changing = [HistoryCreate(**i) for i in normalized_df.to_dict("records")]

    await create_history_changings(session, to_create_history_changing)


async def process_history(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.drop_duplicates(ignore_index=True, inplace=True)
    df.dropna(how='all', inplace=True)
    df.rename(columns={
        'history_version': 'version',
        'history_date': 'date',
        'history_property_name': 'property_name',
        'history_change_type': 'change_type'
    }, inplace=True)
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y %H:%M')
    df = df[list(HistoryCreate.model_fields.keys())]
    df.replace({np.nan: None}, inplace=True)
    return df


async def get_entity_histories(session: AsyncSession, paging: PagingFilter | None = None) -> list[HistoryOut]:
    return await base_cruds.get_all(session=session, model=EntityChanging, response_model=HistoryOut, paging=paging)


async def create_history_changings(session: AsyncSession, items: list[HistoryCreate]) -> None:
    await base_cruds.create_all(session=session, model=EntityChanging, data=items)




