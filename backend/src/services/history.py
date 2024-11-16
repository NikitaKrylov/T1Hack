from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from src.services.base import file_to_pandas_dataframe


async def import_history_data(session: AsyncSession, file_content: bytes):
    df = file_to_pandas_dataframe(file_content, skip_rows=1)
    normalized_df = await process_history(df)


async def process_history(df: pd.DataFrame):
    df = df.copy()
    df.drop_duplicates(ignore_index=True, inplace=True)
    df.dropna(how='all', inplace=True)

