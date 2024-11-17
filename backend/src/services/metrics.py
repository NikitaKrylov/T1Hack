from concurrent.futures.process import ProcessPoolExecutor

import pandas as pd
import numpy as np
import datetime
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


# К выполнению
def kvipolneniyu_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame, df_history: pd.DataFrame,
                        first_date: datetime.date, second_date: datetime.date):
    # Ensure dates are in datetime format
    first_date = pd.to_datetime(first_date)
    second_date = pd.to_datetime(second_date)

    # Get entity_ids for the specified sprint
    entity_ids = df_sprints[df_sprints['name'] == sprint_name]['entity_id'].unique().astype(int)
    print(len(entity_ids))

    # Filter df_history for relevant entity_ids and 'Статус'
    df_history_filtered = df_history[
        (df_history['entity_id'].isin(entity_ids)) &
        (df_history['property_name'] == 'Статус')
        ].copy()

    # Ensure 'history_date' is datetime and 'history_version' is numeric
    df_history_filtered['date'] = pd.to_datetime(df_history_filtered['date'])
    df_history_filtered['version'] = pd.to_numeric(df_history_filtered['version'], errors='coerce')

    # Split history into before and during the date range
    df_history_pre = df_history_filtered[df_history_filtered['date'] < first_date]
    df_history_in = df_history_filtered[
        (df_history_filtered['date'] >= first_date) &
        (df_history_filtered['date'] <= second_date)
        ]

    # Function to safely extract status
    def extract_status(change):
        if '->' in change:
            return change.split('->')[-1].strip()
        else:
            return change.strip()

    # Get last status before first_date
    df_last_status_pre = df_history_pre.sort_values('version').groupby('entity_id').tail(1)
    df_last_status_pre['last_status_pre'] = df_last_status_pre['history_change'].apply(extract_status)

    # Get last status during [first_date, second_date]
    df_last_status_in = df_history_in.sort_values('version').groupby('entity_id').tail(1)
    df_last_status_in['last_status_in'] = df_last_status_in['history_change'].apply(extract_status)

    # Merge statuses
    df_status = pd.DataFrame({'entity_id': entity_ids})
    df_status = df_status.merge(df_last_status_pre[['entity_id', 'last_status_pre']], on='entity_id', how='left')
    df_status = df_status.merge(df_last_status_in[['entity_id', 'last_status_in']], on='entity_id', how='left')

    # Determine final status
    def get_final_status(row):
        if pd.notnull(row['last_status_in']):
            return row['last_status_in']
        elif pd.notnull(row['last_status_pre']):
            return 'created' if row['last_status_pre'] == 'created' else row['last_status_pre']
        else:
            return 'created'

    df_status['final_status'] = df_status.apply(get_final_status, axis=1)

    # Convert 'entity_id' in df_tasks to int
    df_tasks['entity_id'] = df_tasks['entity_id'].astype(int)

    # Calculate metrics
    created_ids = df_status[df_status['final_status'] == 'created']['entity_id']
    total_ids = df_status['entity_id']

    created_estimation = df_tasks[df_tasks['entity_id'].isin(created_ids)]['estimation'].sum() / 3600
    total_estimation = df_tasks[df_tasks['entity_id'].isin(total_ids)]['estimation'].sum() / 3600

    # Return the final metric
    return round(created_estimation, 1), round((created_estimation / total_estimation) * 100, 1)


# В работе
def vrabote_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame, df_history: pd.DataFrame,
                   first_date: datetime.date, second_date: datetime.date):
    # Преобразуем даты в формат datetime
    first_date = pd.to_datetime(first_date)
    second_date = pd.to_datetime(second_date)

    # Получаем список entity_id для указанного спринта
    entity_ids = df_sprints[df_sprints['name'] == sprint_name]['entity_id'].unique().astype(int)

    # Фильтруем df_history по соответствующим entity_id и 'Статус'
    df_history_filtered = df_history[
        (df_history['entity_id'].isin(entity_ids)) &
        (df_history['property_name'] == 'Статус')
        ].copy()

    # Убеждаемся, что 'history_date' и 'history_version' имеют правильные типы данных
    df_history_filtered['date'] = pd.to_datetime(df_history_filtered['date'])
    df_history_filtered['version'] = pd.to_numeric(df_history_filtered['version'], errors='coerce')

    # Разделяем историю на до и во время указанного диапазона дат
    df_history_pre = df_history_filtered[df_history_filtered['date'] < first_date]
    df_history_in = df_history_filtered[
        (df_history_filtered['date'] >= first_date) &
        (df_history_filtered['date'] <= second_date)
        ]

    # Функция для безопасного извлечения статуса
    def extract_status(change):
        if '->' in change:
            return change.split('->')[-1].strip()
        else:
            return change.strip()

    # Получаем последний статус до first_date
    df_last_status_pre = df_history_pre.sort_values('version').groupby('entity_id').tail(1)
    df_last_status_pre['last_status_pre'] = df_last_status_pre['history_change'].apply(extract_status)

    # Получаем последний статус в период [first_date, second_date]
    df_last_status_in = df_history_in.sort_values('version').groupby('entity_id').tail(1)
    df_last_status_in['last_status_in'] = df_last_status_in['history_change'].apply(extract_status)

    # Объединяем статусы
    df_status = pd.DataFrame({'entity_id': entity_ids})
    df_status = df_status.merge(df_last_status_pre[['entity_id', 'last_status_pre']], on='entity_id', how='left')
    df_status = df_status.merge(df_last_status_in[['entity_id', 'last_status_in']], on='entity_id', how='left')

    # Определяем финальный статус
    def get_final_status(row):
        if pd.notnull(row['last_status_in']):
            return row['last_status_in']
        elif pd.notnull(row['last_status_pre']):
            return row['last_status_pre']
        else:
            return 'created'

    df_status['final_status'] = df_status.apply(get_final_status, axis=1)

    # Получаем список entity_id, которые не имеют статус "closed" или "done"
    not_closed_ids = df_status[~df_status['final_status'].isin(['closed', 'done'])]['entity_id']
    total_ids = df_status['entity_id']

    # Убеждаемся, что 'entity_id' в df_tasks имеет тип int
    df_tasks['entity_id'] = df_tasks['entity_id'].astype(int)

    # Вычисляем метрики
    mot_closed = df_tasks[df_tasks['entity_id'].isin(not_closed_ids)]['estimation'].sum() / 3600
    total_estimation = df_tasks[df_tasks['entity_id'].isin(total_ids)]['estimation'].sum() / 3600

    # Возвращаем итоговую метрику в %
    return round(mot_closed, 1), round((mot_closed / total_estimation) * 100, 1)


# Сделано
def sdelano_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame,
                   df_history: pd.DataFrame, first_date: datetime.date, second_date: datetime.date):
    # Преобразование дат в datetime
    first_date = pd.to_datetime(first_date)
    second_date = pd.to_datetime(second_date)

    # Убедимся, что 'entity_id' и другие поля имеют корректные типы
    df_sprints['entity_id'] = df_sprints['entity_id'].astype(int)
    df_tasks['entity_id'] = df_tasks['entity_id'].astype(int)
    df_history['entity_id'] = df_history['entity_id'].astype(int)
    df_history['date'] = pd.to_datetime(df_history['date'])
    df_history['version'] = pd.to_numeric(df_history['version'], errors='coerce')

    # Получение entity_id по условиям
    list_entity_1 = df_tasks[df_tasks["type"].isin(["Задача", "Дефектов"])]["entity_id"].unique()
    entity_ids = df_sprints[df_sprints["name"] == sprint_name]["entity_id"].unique()
    list_entity_2 = df_history[(df_history["date"] >= first_date) &
                               (df_history["date"] <= second_date)]["entity_id"].unique()

    # Пересечение всех entity_id
    main_list = set(list_entity_1).intersection(list_entity_2, entity_ids)

    # Фильтрация истории только для задач из main_list
    df_history_filtered = df_history[
        (df_history["entity_id"].isin(main_list)) &
        (df_history["property_name"] == "Статус")
        ]

    # Получение последнего статуса для каждого entity_id
    df_last_status = (df_history_filtered.sort_values("version")
                      .groupby("entity_id")
                      .tail(1)
                      .assign(last_status=lambda x: x["history_change"].str.split("-> ").str[-1].str.strip()))

    # Фильтрация по статусам "closed" и "done"
    res_entity_id = df_last_status[df_last_status["last_status"].isin(["closed", "done"])]["entity_id"].unique()

    # Вычисление времени задач со статусами "closed" или "done"
    created_done = df_tasks[df_tasks["entity_id"].isin(res_entity_id)]["estimation"].sum() / 3600

    # Вычисление времени всех задач из main_list
    all_estimation = df_tasks[df_tasks["entity_id"].isin(main_list)]["estimation"].sum() / 3600

    # Возвращаем итоговую метрику в процентах
    return round(created_done, 1), round((created_done / all_estimation) * 100, 1)


# Снято
def snyato_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame,
                  df_history: pd.DataFrame, first_date: datetime.date, second_date: datetime.date):
    # Преобразуем даты в формат datetime
    first_date = pd.to_datetime(first_date)
    second_date = pd.to_datetime(second_date)

    # Убедимся, что 'entity_id' имеет тип int во всех DataFrame
    df_sprints['entity_id'] = df_sprints['entity_id'].astype(int)
    df_tasks['entity_id'] = df_tasks['entity_id'].astype(int)
    df_history['entity_id'] = df_history['entity_id'].astype(int)

    # Преобразуем 'history_date' в datetime и 'history_version' в numeric
    df_history['date'] = pd.to_datetime(df_history['date'])
    df_history['version'] = pd.to_numeric(df_history['version'], errors='coerce')

    # Получаем entity_ids для указанного спринта
    entity_ids = df_sprints[df_sprints['name'] == sprint_name]['entity_id'].unique()

    # Фильтруем df_tasks для этих entity_ids
    df_tasks_filtered = df_tasks[df_tasks['entity_id'].isin(entity_ids)][
        ['entity_id', 'type', 'status', 'estimation']].drop_duplicates()

    # Фильтруем df_history для этих entity_ids и указанного диапазона дат
    df_history_filtered = df_history[
        (df_history['entity_id'].isin(entity_ids)) &
        (df_history['date'] >= first_date) &
        (df_history['date'] <= second_date)
        ]

    # Получаем последний 'Статус' для каждого entity_id
    status_df = df_history_filtered[df_history_filtered['property_name'] == 'Статус']
    status_df = status_df.sort_values('version')
    status_last = status_df.groupby('entity_id').tail(1)
    status_last = status_last.copy()
    status_last['last_status'] = status_last['history_change'].apply(lambda x: x.split('-> ')[-1].strip())

    # Получаем последнюю 'Резолюция' для каждого entity_id
    resolution_df = df_history_filtered[df_history_filtered['property_name'] == 'Резолюция']
    resolution_df = resolution_df.sort_values('version')
    resolution_last = resolution_df.groupby('entity_id').tail(1)
    resolution_last['last_resolution'] = resolution_last['history_change'].apply(lambda x: x.split('-> ')[-1].strip())

    # Объединяем данные в один DataFrame
    df_merged = df_tasks_filtered.merge(status_last[['entity_id', 'last_status']], on='entity_id', how='left')
    df_merged = df_merged.merge(resolution_last[['entity_id', 'last_resolution']], on='entity_id', how='left')

    # Определяем финальный статус и резолюцию для каждого entity_id
    def determine_status(row):
        if row['type'] == 'Дефект':
            if row['status'] == 'Отклонен исполнителем':
                return pd.Series({'status_final': 'closed', 'resolution_final': 'Отклонено'})
            else:
                return pd.Series({'status_final': '-', 'resolution_final': None})
        elif pd.notnull(row['last_status']) and pd.notnull(row['last_resolution']):
            return pd.Series({'status_final': row['last_status'], 'resolution_final': row['last_resolution']})
        else:
            return pd.Series({'status_final': 'created', 'resolution_final': None})

    df_merged[['status_final', 'resolution_final']] = df_merged.apply(determine_status, axis=1)

    # Получаем entity_id со статусами 'closed' или 'done'
    statuscloseddone_ids = df_merged[df_merged['status_final'].isin(['closed', 'done'])]['entity_id']

    # Получаем entity_id с резолюцией 'Отклонено', 'Отменено инициатором' или 'Дубликат'
    resolutiondeny_ids = \
    df_merged[df_merged['resolution_final'].isin(['Отклонено', 'Отменено инициатором', 'Дубликат'])]['entity_id']

    # Находим пересечение entity_id, удовлетворяющих обоим условиям
    common_ids = set(statuscloseddone_ids) & set(resolutiondeny_ids)

    # Вычисляем 'created_done'
    created_done = df_tasks[df_tasks['entity_id'].isin(common_ids)]['estimation'].sum() / 3600

    # Вычисляем 'all_estimation'
    all_estimation = df_tasks[df_tasks['entity_id'].isin(entity_ids)]['estimation'].sum() / 3600

    # Возвращаем итоговую метрику в процентах
    return round(created_done, 1), round((created_done / all_estimation) * 100, 1)


# Заблокировано
def blockedtasksCHD_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame,
                           df_history: pd.DataFrame, first_date: datetime.date, second_date: datetime.date):
    # Заполнение пустых значений в 'history_change'
    df_history['history_change'] = df_history['history_change'].fillna(' -> ')

    # Получаем entity_ids для указанного спринта
    entity_ids = df_sprints[df_sprints['name'] == sprint_name]['entity_id'].unique()

    # Фильтруем историю по указанным entity_ids и диапазону дат
    df_history_filtered = df_history[
        (df_history['entity_id'].isin(entity_ids)) &
        (df_history['date'] >= first_date) &
        (df_history['date'] <= second_date)
        ]

    # Обрабатываем статусы
    status_df = df_history_filtered[df_history_filtered['property_name'] == 'Статус']
    status_df = status_df.sort_values('version').groupby('entity_id').tail(1)
    status_df['entity_status'] = status_df['history_change'].apply(lambda x: x.split('-> ')[-1].strip())

    # Обрабатываем связанные задачи
    bind_df = df_history_filtered[df_history_filtered['property_name'] == 'Связанные Задачи'].copy()
    bind_df['is_locked'] = bind_df['history_change'].str.contains('lock')

    # Считаем количество заблокированных задач для каждого entity_id
    bind_counts = bind_df.groupby('entity_id')['is_locked'].sum()

    # Объединяем данные
    merged = pd.DataFrame({'entity_id': entity_ids})
    merged = merged.merge(status_df[['entity_id', 'entity_status']], on='entity_id', how='left')
    merged = merged.merge(bind_counts, on='entity_id', how='left').fillna({'is_locked': 0})

    # Применяем логику вычисления статуса
    merged['is_blocked'] = merged.apply(
        lambda row: 1 if row['entity_status'] not in ['done'] and row['is_locked'] > 0 else 0, axis=1
    )

    # Возвращаем итоговое количество заблокированных задач
    return merged['is_blocked'].sum()


def dobavleno_chd_sht(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame, df_history: pd.DataFrame,
                      first_date: datetime.date, second_date: datetime.date):
    line_history_pieces = []
    line_history_hour = []
    line_history_hour_for_8 = []

    df_history['history_change'] = df_history['history_change'].fillna(' -> ')

    # Преобразуем строки в даты
    day_one = first_date
    day_two = second_date
    # min(df_sprints[df_sprints["sprint_name"] == sprint_name].sprint_start_date)
    # max(df_sprints[df_sprints["sprint_name"] == sprint_name].sprint_end_date)

    ids = df_sprints[df_sprints["name"] == sprint_name].entity_id.to_list()
    list_all = []
    difference_in_days = (day_two - day_one).days
    # подсчитаем сколько было создано до начало спринта
    for i in range(difference_in_days):
        data_now = day_one + datetime.timedelta(days=i)
        k = df_history[(df_history["date"] == data_now) & (df_history["entity_id"].isin(ids) & (
                df_history["change_type"] == "CREATED"))].entity_id.to_list()
        list_all.extend(k)

    list_transferred_id = set()
    list_present_id = set(ids) - set(list_all)
    pre_count_entity = len(list_present_id)
    list_all = []
    filtered_df_2 = df_history[(df_history["date"] >= day_one) & (df_history["date"] <= day_two) & (
        df_history["entity_id"].isin(ids))]

    for i in range(difference_in_days):
        data_now = day_one + datetime.timedelta(days=i)
        filtered_df = df_history[(df_history["date"] == data_now) & (
                df_history["entity_id"].isin(ids) & (df_history["change_type"] == "CREATED"))]
        k_count = filtered_df.entity_id.to_list()

        # посмотрим какие id были удалены в этот день или изменены в другой спринт
        status_dict = {}
        resolution_dict = {}
        filtered_df_1 = df_history[(df_history["date"] == data_now) & (df_history["entity_id"].isin(ids))]
        status_df = filtered_df_1[filtered_df_1['property_name'] == "Статус"]
        for entity_id in k_count:

            resolution_df = filtered_df_2[
                (filtered_df_2['property_name'] == "Резолюция") & (filtered_df_2["entity_id"] == entity_id)]
            if not status_df.empty and not resolution_df.empty:
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
        # Получаем список entity_id, которые имеют статус "closed","done"
        resolutiondeny_ids = [key for key, value in resolution_dict.items() if
                              value in ['Отклонено', 'Отменено инициатором', 'Дубликат']]
        common_ids = set(statuscloseddone_ids) & set(resolutiondeny_ids)

        all_changes_plus = set()
        all_changes_del = set()
        # смотрим какие id появились в спринте
        filtered_df = df_history[(df_history["date"] == data_now) & (df_history["entity_id"].isin(ids))]
        for i in list_transferred_id:
            status_df = filtered_df[
                (filtered_df['property_name'] == "Спринт") & (filtered_df["entity_id"] == i)]
            if not status_df.empty:
                max_version_row = status_df.loc[status_df['version'].idxmax()]
                history_change = max_version_row['history_change']
                if sprint_name in history_change.split(" -> ")[1].strip():
                    all_changes_plus.add(i)

        # смотрим какие id были перенесен в другой спринт
        for i in set(k_count) - set(common_ids):
            status_df = filtered_df[
                (filtered_df['property_name'] == "Спринт") & (filtered_df["entity_id"] == i)]
            if not status_df.empty:
                max_version_row = status_df.loc[status_df['version'].idxmax()]
                history_change = max_version_row['history_change']
                if sprint_name not in history_change.split(" -> ")[1].strip():
                    all_changes_del.add(i)

        dop_k = 0
        dop_k -= len(all_changes_del)
        list_transferred_id = list_transferred_id | all_changes_del
        if len(all_changes_plus & list_transferred_id) != 0:
            dop_k += len(all_changes_plus & list_transferred_id)
        list_transferred_id = list_transferred_id - all_changes_plus
        list_all.append(len(k_count) - len(common_ids) + dop_k)
        filtered_df = df_tasks[df_tasks['entity_id'].isin(int(x) for x in (
                set(k_count) - common_ids | (all_changes_plus & list_transferred_id) - all_changes_del))]
        line_history_hour_for_8.append(filtered_df['estimation'].sum() / 3600)

        # подсчитаем метрику №7
        line_history_pieces.append(
            (len(k_count) + len(all_changes_plus & list_transferred_id), len(common_ids) + len(all_changes_del)))
        dop_hour, minus_hour = 0, 0
        filtered_df = df_tasks[
            df_tasks['entity_id'].isin(int(x) for x in (set(k_count) | (all_changes_plus & list_transferred_id)))]
        dop_hour = filtered_df['estimation'].sum() / 3600
        filtered_df = df_tasks[df_tasks['entity_id'].isin(int(x) for x in (common_ids | all_changes_del))]
        minus_hour = filtered_df['estimation'].sum() / 3600
        line_history_hour.append((dop_hour, minus_hour))

    list_all[0] += pre_count_entity
    return (line_history_pieces, line_history_hour), (list_all, line_history_hour_for_8)


# бэклог с начала спринта изменён на ... (5)
def backlogchange_metric(sprint_name: str, df_sprints: pd.DataFrame, df_tasks: pd.DataFrame, df_history: pd.DataFrame,
                         first_date: datetime.date, second_date: datetime.date):
    first_date = first_date + datetime.timedelta(days=2)  #прибавляю 2 дня к первой дате
    #создаю лист c entity_id из этого спринта
    entity_ids = []
    for index, row in df_sprints.iterrows():
        if row['name'] == sprint_name:
            entity_ids.append(row['entity_id'])

    # вычисляю количество объектов, добавленных на последний день
    tmp_df = df_history[(df_history['date'].dt.date <= second_date) & (df_history['date'].dt.date > first_date) & (
                df_history['change_type'] == 'CREATED')]
    tmp_df = tmp_df[tmp_df['entity_id'].isin(entity_ids)]
    ids_day_last = tmp_df['entity_id'].tolist()

    # вычисляю просто количство объектов, добавленных в спринт до его начала и в течение двух дней после дня включительно
    tmp_df = df_history[(df_history['date'].dt.date <= first_date) & (df_history['change_type'] == 'CREATED')]
    tmp_df = tmp_df[tmp_df['entity_id'].isin(entity_ids)]
    ids = tmp_df['entity_id'].tolist()

    # Фильтруем DataFrame
    day_last = df_tasks[df_tasks['entity_id'].isin(int(x) for x in ids_day_last)]['estimation'].sum() / 3600
    ids = df_tasks[df_tasks['entity_id'].isin(int(x) for x in ids)]['estimation'].sum() / 3600

    # возвращаю итоговую метрику в %
    return round(day_last, 1), round(day_last / ids * 100, 1)


def not_completed_tasks_at_day(sprint_name: str, df_sprints: pd.DataFrame, df_history: pd.DataFrame, first_date: datetime.date, second_date: datetime.date):
    entity_ids = df_sprints[df_sprints["name"] == sprint_name].entity_id.to_list()
    date_count = {}
    date_range = pd.date_range(start=first_date, end=second_date, freq='D')
    for single_date in date_range:
        entity_ids_history = df_history[(df_history['entity_id'].isin(entity_ids)) & \
                                        (df_history['date'] == single_date) & \
                                        (df_history['property_name'] == 'Статус') & \
                                        (df_history['history_change_after'] == 'inProgress')] \
                                        .drop_duplicates(subset=['entity_id'])
        date_count[f'{single_date}'[:10]] = float(entity_ids_history['entity_id'].count())
    return date_count


def KPI_total_tasks(sprint_name: str, df_sprints: pd.DataFrame, df_history: pd.DataFrame, first_date: datetime.date, second_date: datetime.date):
    entity_ids_for_sprint = df_sprints[df_sprints["name"] == sprint_name].entity_id.to_list() #отбор entity
    entity_ids_in_date = df_history[(df_history['date'].dt.date >= first_date ) & (df_history['date'].dt.date <= second_date)]['entity_id'].drop_duplicates()
    entity_ids = entity_ids_in_date[entity_ids_in_date.isin(entity_ids_for_sprint)]
    return len(entity_ids)

 # KPI Выполнено задач (2)
def KPI_completed_tasks(sprint_name: str, df_sprints: pd.DataFrame, df_history: pd.DataFrame, first_date: datetime.date, second_date: datetime.date):
    entity_ids = df_sprints[df_sprints["name"] == sprint_name].entity_id.to_list()
    entity_ids_history = df_history[(df_history['entity_id'].isin(entity_ids)) & \
                                    (df_history['date'].dt.date >= first_date) & (df_history['date'].dt.date <= second_date) & \
                                    (df_history['property_name'] == 'Статус') & \
                                    (df_history['history_change_after'] == 'closed')].drop_duplicates(subset=['entity_id'])
    return entity_ids_history['entity_id'].count()


async def get_sprint_metrics(session: AsyncSession, sprint_id: int, first_date: datetime.date,
                             second_date: datetime.date):
    sprint = await base_cruds.get_one_or_none_by_id(session=session, model=Sprint, response_model=SprintOut,
                                                    _id=sprint_id)

    if not sprint:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'Спринт с id({sprint_id}) не найден')

    all_sprints = await get_entity_id_with_sprints(session=session)
    all_sprints_df = pd.DataFrame(all_sprints)

    all_history = await get_entity_histories(session=session)
    all_history_df = pd.DataFrame([i.model_dump() for i in all_history])
    all_history_df['date'] = all_history_df['date'].dt.date
    all_history_df[['history_change_before', 'history_change_after']] = all_history_df['history_change'].str.split(' -> ', n=1, expand=True)
    # df_history_split = df_history.drop(columns={'history_change'})
    # all_history_df.dropna(inplace=True)

    all_tasks = await get_entities_list(session)
    all_tasks_df = pd.DataFrame([i.model_dump() for i in all_tasks])
    all_tasks_df = all_tasks_df.drop_duplicates(subset=[col for col in all_tasks_df.columns if col not in ["sprint_id", "id"]],ignore_index=True)


    metrics_data = {
        'sprint_name': sprint.name,
        'df_sprints': all_sprints_df,
        'df_tasks': all_tasks_df,
        'df_history': all_history_df,
        'first_date': first_date,
        'second_date': second_date
    }

    _dobavleno_chd_sht = dobavleno_chd_sht(**metrics_data)

    _blockedtasksCHD_metric = blockedtasksCHD_metric(**metrics_data)

    _snyato_metric = snyato_metric(**metrics_data)

    _sdelano_metric = sdelano_metric(**metrics_data)

    _vrabote_metric = vrabote_metric(**metrics_data)

    _kvipolneniyu_metric = kvipolneniyu_metric(**metrics_data)

    _backlogchange_metric = backlogchange_metric(**metrics_data)

    _KPI_total_tasks = KPI_total_tasks(
        sprint_name=sprint.name,
        df_sprints=all_sprints_df,
        df_history=all_history_df,
        first_date=first_date,
        second_date=second_date
    )

    _not_completed_tasks_at_day = not_completed_tasks_at_day(
        sprint_name=sprint.name,
        df_sprints=all_sprints_df,
        df_history=all_history_df,
        first_date=first_date,
        second_date=second_date
    )

    _KPI_completed_tasks = KPI_completed_tasks(
        sprint_name=sprint.name,
        df_sprints=all_sprints_df,
        df_history=all_history_df,
        first_date=first_date,
        second_date=second_date
    )


    result = {
        'dobavleno_chd_sht': _dobavleno_chd_sht,
        'blockedtasksCHD_metric': float(_blockedtasksCHD_metric),
        'snyato_metric': _snyato_metric,
        'sdelano_metric': _sdelano_metric,
        'vrabote_metric': _vrabote_metric,
        'kvipolneniyu_metric': _kvipolneniyu_metric,
        'backlogchange_metric': _backlogchange_metric,
        'not_completed_tasks_at_day': _not_completed_tasks_at_day,
        'KPI_total_tasks': _KPI_total_tasks,
        'KPI_completed_tasks': int(_KPI_completed_tasks)
    }

    return result


