from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from src.database.cruds import base as base_cruds
from src.database.models import EntityChanging
from src.schemas.filters import PagingFilter
from src.schemas.history import HistoryOut
from src.services.base import file_to_pandas_dataframe


async def import_history_data(session: AsyncSession, file_content: bytes):
    df = file_to_pandas_dataframe(file_content, skip_rows=1)
    normalized_df = await process_history(df)


async def process_history(df: pd.DataFrame):
    df = df.copy()
    df.drop_duplicates(ignore_index=True, inplace=True)
    df.dropna(how='all', inplace=True)


async def get_entity_histories(session: AsyncSession, paging: PagingFilter | None = None) -> list[HistoryOut]:
    return await base_cruds.get_all(session=session, model=EntityChanging, response_model=HistoryOut, paging=paging)





