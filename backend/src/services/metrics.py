from concurrent.futures.process import ProcessPoolExecutor

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.cruds import base as base_cruds
from src.database.cruds.sprints import get_entity_id_with_sprints
from src.schemas.filters import EntityHistoryFilter
from src.services.entities import get_entities_list
from src.database.models import Sprint
from src.schemas.sprints import SprintOut
from starlette import status
from http.client import HTTPException
from src.services.sprints import get_sprints_list
from src.services.history import get_entity_histories
import asyncio


# Заблокировано задач в Ч/Д (6)
# Заблокировано задач в Ч/Д (6)
def blockedtasksCHD_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame, df_history: pd.DataFrame, first_date: datetime.date, second_date: datetime.date):
    #создаю лист c entity_id из этого спринта
    entity_ids = []
    for index, row in df_sprints.iterrows():
        if row['name'] == sprint_name:
            entity_ids.append(row['entity_id'])

    status_bind = {}
    for entity_id in entity_ids:
        #статус для entity
        entity_id_history = df_history[(df_history['entity_id'] == entity_id) & (df_history['date'] >= first_date ) & (df_history['date'] <= second_date)]
        tmp = entity_id_history[entity_id_history["property_name"] == "Статус"]
        if tmp.empty:
            entity_id_status = 'created'
        else:
            entity_id_status = tmp.loc[tmp["version"].idxmax()]['history_change'].split('-> ')[1].strip()
        tmp = entity_id_history[entity_id_history["property_name"] == "Связанные Задачи"]
        if tmp.empty:
            entity_id_bind = 0
        else:
            entity_id_bind = entity_id_history[entity_id_history['history_change'].str.contains('lock')]['history_change'].count()
        status_bind[f'{entity_id}'] = 1 if entity_id_status not in ['done'] and entity_id_bind > 0 else 0
    return sum(1 for value in status_bind.values() if value == 1)


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


# к выполнению (1)
def kvipolneniyu_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame, df_history: pd.DataFrame,
                        first_date: date, second_date: date):
    #создаю лист c entity_id, которые будем проверять на "created"
    entity_ids = []
    for index, row in df_sprints.iterrows():
        if row['name'] == sprint_name:
            entity_ids.append(row['entity_id'])

    #создаю словарь и записываю в него {'entity_id': 'status'}
    status_dict = {}
    for entity_id in entity_ids:
        # посмотрим на последний статус задачи до нашего спринта
        filtered_df_pre = df_history[(df_history['entity_id'] == entity_id) & (df_history['date'] < first_date)]
        status_df_pre = filtered_df_pre[filtered_df_pre['property_name'] == "Статус"]
        if not status_df_pre.empty:
            # Находим максимальное значение в колонке "history_version"
            max_version_row = status_df_pre.loc[status_df_pre['version'].idxmax()]
            # Извлекаем значение из столбца "history_change" после "-> "
            history_change = max_version_row['history_change']
            last_status = history_change.split('-> ')[1].strip()
        else:
            # нет было других статусов
            last_status = ""
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
            if last_status != "":
                if last_status == "created":
                    status_dict[f'{entity_id}'] = "created"
                else:
                    status_dict[f'{entity_id}'] = last_status
            else:
                status_dict[f'{entity_id}'] = "created"

    # Получаем список entity_id, которые имеют статус "created" и просто всех entity_id
    created_ids = [key for key, value in status_dict.items() if value == "created"]
    ids = status_dict.keys()
    # Фильтруем DataFrame
    filtered_df = df_tasks[df_tasks['entity_id'].isin(int(x) for x in created_ids)]
    created = filtered_df['estimation'].sum() / 3600
    filtered_df2 = df_tasks[df_tasks['entity_id'].isin(int(x) for x in ids)]
    total_by_ids = filtered_df2['estimation'].sum() / 3600
    # возвращаю итоговую метрику в %
    return (created / total_by_ids) * 100


# в работе (2) [пройденный спринт]
def vrabote_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame, df_history: pd.DataFrame,
                   first_date: datetime.date, second_date: datetime.date):
    #создаю лист c entity_id, которые будем проверять на "created"
    entity_ids = []
    for index, row in df_sprints.iterrows():
        if row['name'] == sprint_name:
            entity_ids.append(row['entity_id'])

    #создаю словарь и записываю в него {'entity_id': 'status'}
    status_dict = {}
    for entity_id in entity_ids:
        # посмотрим на последний статус задачи до нашего спринта
        filtered_df_pre = df_history[(df_history['entity_id'] == entity_id) & (df_history['date'] < first_date)]
        status_df_pre = filtered_df_pre[filtered_df_pre['property_name'] == "Статус"]
        if not status_df_pre.empty:
            # Находим максимальное значение в колонке "history_version"
            max_version_row = status_df_pre.loc[status_df_pre['version'].idxmax()]
            # Извлекаем значение из столбца "history_change" после "-> "
            history_change = max_version_row['history_change']
            last_status = history_change.split('-> ')[1].strip()
        else:
            # нет было других статусов
            last_status = ""
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
            if last_status != "":
                status_dict[f'{entity_id}'] = last_status
            else:
                status_dict[f'{entity_id}'] = "created"

    # Получаем список entity_id, которые не имеют статус "closed", "done"
    created_ids = [key for key, value in status_dict.items() if value != "closed" and value != "done"]
    ids = status_dict.keys()
    # Фильтруем DataFrame
    filtered_df = df_tasks[df_tasks['entity_id'].isin(int(x) for x in created_ids)]
    mot_closed = filtered_df['estimation'].sum() / 3600
    filtered_df2 = df_tasks[df_tasks['entity_id'].isin(int(x) for x in ids)]
    total_by_ids = filtered_df2['estimation'].sum() / 3600
    # возвращаю итоговую метрику в %
    return (mot_closed / total_by_ids) * 100


# сделано (3) [пройденный спринт]
def sdelano_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame, df_history: pd.DataFrame,
                   first_date: datetime.date, second_date: datetime.date):
    # берем только те entity_id, которые в истории последнее действие
    list_entity_1 = df_tasks[
        (df_tasks["type"].isin(["Задача", "Дефектов"]))
    ].entity_id

    list_entity_2 = df_history[(df_history['date'] >= first_date) & (df_history['date'] <= second_date)].entity_id
    main_list = set(list_entity_1) & set(list_entity_2)
    # теперь нужно взять последние статусы у задач
    status_dict = {}
    for entity_id in main_list:
        filtered_df = df_history[(df_history['entity_id'] == entity_id)]
        status_df = filtered_df[filtered_df['property_name'] == "Статус"]
        if not status_df.empty:
            # Находим максимальное значение в колонке "history_version"
            max_version_row = status_df.loc[status_df['version'].idxmax()]
            # Извлекаем значение из столбца "history_change" после "-> "
            history_change = max_version_row['history_change']
            last_status = history_change.split('-> ')[1].strip()
            if last_status == "closed":
                status_dict[entity_id] = "closed"
            elif last_status == "done":
                status_dict[entity_id] = "done"

    # подсчитаем время задач, которые “Закрыто”, “Выполнено”
    res_entity_id = list(status_dict.keys())
    filtered_df = df_tasks[df_tasks['entity_id'].isin(int(x) for x in res_entity_id)]
    created_done = filtered_df['estimation'].sum() / 3600
    # подсчитаем время задач, которое не “Закрыто”, “Выполнено”
    # missing_entity_id = main_list - set(status_dict.keys())
    filtered_df = df_tasks[df_tasks['entity_id'].isin(int(x) for x in main_list)]
    all_estimation = filtered_df['estimation'].sum() / 3600

    return (created_done / all_estimation) * 100


# снято (4)
def snyato_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame, df_history: pd.DataFrame,
                  first_date: datetime.date, second_date: datetime.date):
    #создаю лист c entity_id из этого спринта
    entity_ids = []
    for index, row in df_sprints.iterrows():
        if row['name'] == sprint_name:
            entity_ids.append(row['entity_id'])

    #создаю словарь и записываю в него {'entity_id': 'status'}
    status_dict = {}
    resolution_dict = {}
    for entity_id in entity_ids:
        # Фильтруем строки по entity_id и времени
        filtered_df = df_history[(df_history['entity_id'] == entity_id) & (df_history['date'] >= first_date) & (
                    df_history['date'] <= second_date)]
        # проверка на дефект
        type_name = df_tasks[df_tasks["entity_id"] == entity_id]
        # Проверяем наличие "Статус" в колонке "history_property_name"
        status_df = filtered_df[filtered_df['property_name'] == "Статус"]
        resolution_df = filtered_df[filtered_df['property_name'] == "Резолюция"]
        if type_name["type"].iloc[0] == "Дефект":
            if type_name["status"].iloc[0] == "Отклонен исполнителем":
                status_dict[f'{entity_id}'] = "closed"
                resolution_dict[f'{entity_id}'] = "Отклонено"
            else:
                status_dict[f'{entity_id}'] = "-"
        elif not status_df.empty and not resolution_df.empty:
            # Находим максимальное значение в колонке "history_version"
            max_version_row1 = status_df.loc[status_df['version'].idxmax()]
            max_version_row2 = resolution_df.loc[resolution_df['version'].idxmax()]
            # Извлекаем значение из столбца "history_change" после "-> "
            history_change1 = max_version_row1['history_change']
            history_change2 = max_version_row2['history_change']
            status_dict[f'{entity_id}'] = history_change1.split('-> ')[1].strip()
            resolution_dict[f'{entity_id}'] = history_change2.split('-> ')[1].strip()
        else:
            status_dict[f'{entity_id}'] = "created"

    # Получаем список entity_id, которые имеют статус "closed","done" и просто всех entity_id
    statuscloseddone_ids = [key for key, value in status_dict.items() if value in ["closed", "done"]]
    ids = status_dict.keys()
    # Получаем список entity_id, которые имеют статус "closed","done"
    resolutiondeny_ids = [key for key, value in resolution_dict.items() if
                          value in ['Отклонено', 'Отменено инициатором', 'Дубликат']]
    # Смотрю, есть ли в created_ids резолюция = (Отклонено, Отменено инициатором, Дубликат)
    common_ids = set(statuscloseddone_ids) & set(resolutiondeny_ids)

    filtered_df = df_tasks[df_tasks['entity_id'].isin(int(x) for x in common_ids)]
    created_done = filtered_df['estimation'].sum() / 3600

    filtered_df = df_tasks[df_tasks['entity_id'].isin(int(x) for x in entity_ids)]
    all_estimation = filtered_df['estimation'].sum() / 3600

    return (created_done / all_estimation) * 100


# бэклог с начала спринта изменён на ... (5)
def backlogchange_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame, df_history: pd.DataFrame,
                         first_date: datetime.date):
    second_date = first_date + timedelta(days=2)  #создаю вторую дату
    #создаю лист c entity_id из этого спринта
    entity_ids = []
    for index, row in df_sprints.iterrows():
        if row['name'] == sprint_name:
            entity_ids.append(row['entity_id'])

    # вычисляю количество объектов, добавленных на 2ой день
    tmp_df = df_history[(df_history['date'] == second_date) & (df_history['change_type'] == 'CREATED')]
    tmp_df = tmp_df[tmp_df['entity_id'].isin(entity_ids)]
    ids_day2 = tmp_df['entity_id'].tolist()

    # вычисляю просто количство объектов, добавленных в спринт до 2го дня включительно
    tmp_df = df_history[(df_history['date'] <= second_date) & (df_history['change_type'] == 'CREATED')]
    tmp_df = tmp_df[tmp_df['entity_id'].isin(entity_ids)]
    ids = tmp_df['entity_id'].tolist()

    # Фильтруем DataFrame
    day2 = df_tasks[df_tasks['entity_id'].isin(int(x) for x in ids_day2)]['estimation'].sum() / 3600
    ids = df_tasks[df_tasks['entity_id'].isin(int(x) for x in ids)]['estimation'].sum() / 3600

    # возвращаю итоговую метрику в %
    return round(day2 / ids * 100, 1)


async def get_blockedtasksCHD_metricx(session: AsyncSession, sprint_id: int, first_date: date, second_date: date):
    first_time = datetime.now()

    sprint = await base_cruds.get_one_or_none_by_id(session=session, model=Sprint, response_model=SprintOut,
                                                    _id=sprint_id)

    if not sprint:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'Спринт с id({sprint_id}) не найден')

    all_sprints = await get_entity_id_with_sprints(session=session)
    all_sprints_df = pd.DataFrame(all_sprints)

    all_history = await get_entity_histories(session=session)
    all_history_df = pd.DataFrame([i.model_dump() for i in all_history])
    all_history_df['date'] = all_history_df['date'].dt.date
    all_history_df.dropna(inplace=True)

    all_tasks = await get_entities_list(session)
    all_tasks_df = pd.DataFrame([i.model_dump() for i in all_tasks])


    # OK
    result = kvipolneniyu_metric(
        sprint_name=sprint.name,
        first_date=first_date,
        second_date=second_date,
        df_sprints=all_sprints_df,
        df_history=all_history_df,
        df_tasks=all_tasks_df
    )

    # OK
    # result = vrabote_metric(
    #     sprint_name=sprint.name,
    #     first_date=first_date,
    #     second_date=second_date,
    #     df_sprints=all_sprints_df,
    #     df_history=all_history_df,
    #     df_tasks=all_tasks_df
    # )

    # OK
    # result3 = sdelano_metric(
    #     sprint_name=sprint.name,
    #     first_date=first_date,
    #     second_date=second_date,
    #     df_sprints=all_sprints_df,
    #     df_history=all_history_df,
    #     df_tasks=all_tasks_df
    # )

    # OK
    # result2 = snyato_metric(
    #     sprint_name=sprint.name,
    #     first_date=first_date,
    #     second_date=second_date,
    #     df_sprints=all_sprints_df,
    #     df_history=all_history_df,
    #     df_tasks=all_tasks_df
    # )

    # ERROR can by nan
    # result = backlogchange_metric(
    #     sprint_name=sprint.name,
    #     first_date=first_date,
    #     df_sprints=all_sprints_df,
    #     df_history=all_history_df,
    #     df_tasks=all_tasks_df
    # )

    # OK
    # result = blockedtasksCHD_metric(
    #     sprint_name=sprint.name,
    #     first_date=first_date,
    #     second_date=second_date,
    #     df_sprints=all_sprints_df,
    #     df_history=all_history_df,
    #     df_tasks=all_tasks_df
    # )
    return result


    # results = await asyncio.gather(t1, t2, t3)

    # return results
    # return result1, result2, result3

    # PROBLEM
    # return created(
    #     sprint_name=sprint.name,
    #     df_history=all_history_df,
    #     df_sprints=all_sprints_df,
    #     first_date=first_date,
    #     second_date=second_date
    # )

# All time: 0:00:06.443786
# All time: 0:00:06.250171
