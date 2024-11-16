import pandas as pd
import numpy as np
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.cruds import base as base_cruds
from src.database.cruds.sprints import get_entity_id_with_sprints
from src.database.models import Sprint
from src.schemas.sprints import SprintOut
from starlette import status
from http.client import HTTPException
from src.services.sprints import get_sprints_list
from src.services.history import get_entity_histories


# Заблокировано задач в Ч/Д (6)
def blockedtasksCHD_metric(sprint_name: str, df_sprints: pd.DataFrame, df_history: pd.DataFrame, first_date: date, second_date: date):
    #создаю лист c entity_id из этого спринта
    entity_ids = []
    for index, row in df_sprints.iterrows():
        if row['name'] == sprint_name:
            entity_ids.append(row['entity_id'])

    status_bind = {}
    for entity_id in entity_ids:
        #статус для entity
        entity_id_history = df_history[
            (df_history['entity_id'] == entity_id) & (df_history['date'] >= first_date) & (
                        df_history['date'] <= second_date)]
        tmp = entity_id_history[entity_id_history["property_name"] == "Статус"]
        if tmp.empty:
            entity_id_status = 'created'
        else:
            entity_id_status = tmp.loc[tmp["version"].idxmax()]['history_change'].split('-> ')[1].strip()
        tmp = entity_id_history[entity_id_history["property_name"] == "Связанные Задачи"]
        if tmp.empty:
            entity_id_bind = 0
        else:
            # entity_id_history.dropna(inplace=True)
            entity_id_bind = entity_id_history[entity_id_history['history_change'].str.contains('lock')][
                'history_change'].count()
        status_bind[f'{entity_id}'] = 1 if entity_id_status not in ['done'] and entity_id_bind > 0 else 0
    return sum(1 for value in status_bind.values() if value == 1)

# пример для вызова функции: a = blockedtasksCHD_metric("Спринт 2024.3.1", df_sprints, df_history, "2024-07-03", "2024-07-16")


# к выполнению
def created(sprint_name, df_sprints: pd.DataFrame, df_history: pd.DataFrame, first_date: datetime.date,
            second_date: datetime.date):
    # создаю лист c entity_id, которые будем проверять на "created"
    entity_ids = []
    for index, row in df_sprints.iterrows():
        if row['name'] == sprint_name:
            entity_ids.append(row['entity_id'])

    # создаю словарь и записываю в него {'entity_id': 'status'}
    status_dict = {}
    for entity_id in entity_ids:
        # Фильтруем строки по entity_id и времени
        filtered_df = df_history[(df_history['entity_id'] == entity_id) & (df_history['date'] >= first_date) & (
                    df_history['date'] <= second_date)]
        # Проверяем наличие "Статус" в колонке "history_property_name"
        status_df = filtered_df[filtered_df['property_name'] == "Статус"]
        if not status_df.empty:
            # Находим максимальное значение в колонке "history_version"
            max_version_row = status_df.loc[status_df['version'].idxmax()]
            # Извлекаем значение из столбца "history_change" после "-> "
            history_change = max_version_row['history_change']
            status_dict[f'{entity_id}'] = history_change.split('-> ')[1].strip()
        else:
            status_dict[f'{entity_id}'] = "created"

    # Получаем список entity_id, которые имеют статус "created" и просто всех entity_id
    created_ids = [key for key, value in status_dict.items() if value == "created"]
    ids = status_dict.keys()
    # Фильтруем DataFrame
    filtered_df = df_history[df_history['entity_id'].isin(int(x) for x in created_ids)]
    created = filtered_df['estimation'].sum() / 3600
    filtered_df2 = df_history[df_history['entity_id'].isin(int(x) for x in ids)]
    total_by_ids = filtered_df2['estimation'].sum() / 3600
    return created / total_by_ids


async def get_blockedtasksCHD_metricx(session: AsyncSession, sprint_id: int, first_date: date, second_date: date) -> int:
    sprint = await base_cruds.get_one_or_none_by_id(session=session, model=Sprint, response_model=SprintOut, _id=sprint_id)

    if not sprint:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'Спринт с id({sprint_id}) не найден')

    all_sprints = await get_entity_id_with_sprints(session=session)
    all_sprints_df = pd.DataFrame(all_sprints)

    all_history = await get_entity_histories(session=session)
    all_history_df = pd.DataFrame([i.model_dump() for i in all_history])
    all_history_df['date'] = all_history_df['date'].dt.date

    all_history_df.dropna(inplace=True)


    return blockedtasksCHD_metric(
        sprint_name=sprint.name,
        df_sprints=all_sprints_df,
        df_history=all_history_df,
        first_date=first_date,
        second_date=second_date
    )

    # return created(
    #     sprint_name=sprint.name,
    #     df_history=all_history_df,
    #     df_sprints=all_sprints_df,
    #     first_date=first_date,
    #     second_date=second_date
    # )
