import numpy as np
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.cruds import base as crud
from src.database.models import Entity
from src.schemas.entities import EntityCreate
from src.schemas.filters import PagingFilter
from src.services.base import file_to_pandas_dataframe


# async def process_entities(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()
#     df.drop_duplicates(ignore_index=True, inplace=True)
#     df['entity_id'] = df['entity_id'].astype('str')
#     df['parent_ticket_id'] = df['parent_ticket_id'].astype(int, errors='ignore')
#     df['due_date'] = pd.to_datetime(df['due_date'], format='%m/%d/%y').dt.date
#     df.replace({np.nan: None}, inplace=True)
#     df.rename(columns={
#         'create_date': 'created_at',
#         'update_date': 'updated_at',
#     }, inplace=True)
#     df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S.%f')
#     # df['created_at'] = df['created_at'].apply(lambda x: x.to_pydatetime())
#     return df
#
#
# async def import_entities_from_file(session: AsyncSession, file_content: bytes) -> None:
#     df = file_to_pandas_dataframe(file_content, skip_rows=1)
#     normalized_df = await process_entities(df)
#     new_entities = [EntityCreate(**i) for i in normalized_df.to_dict('records')]
#     await create_entities(session, new_entities)
#
#
#
# async def create_entities(session: AsyncSession, entities: list[EntityCreate]) -> None:
#     await crud.create_all(session, model=Entity, data=entities)


from src.database.cruds import base as base_cruds
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Entity
from src.schemas.entities import EntityOut


async def get_entities_list(session: AsyncSession, paging: PagingFilter | None = None) -> list[EntityOut]:
    return await base_cruds.get_all(session=session, model=Entity, response_model=EntityOut, paging=paging)

