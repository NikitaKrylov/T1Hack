from typing import Type
from pydantic import BaseModel
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import Base
from src.schemas.filters import PagingFilter, BaseFilter


async def create_one[T: Base, V: BaseModel](session: AsyncSession, model: Type[T], data: BaseModel, response_model: Type[V] | None, **extra_data) -> V | None:
    new_item = model(**data.model_dump(), **extra_data)
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    if response_model:
        return response_model.model_validate(new_item, from_attributes=True)


async def create_all[T: Base](session: AsyncSession, model: Type[T], data: list[BaseModel], **extra_data) -> None:
    new_items = [model(**i.model_dump(), **extra_data) for i in data]
    session.add_all(new_items)
    await session.commit()


async def get_one_or_none_by_id[T: Base, V: BaseModel](session: AsyncSession, model: Type[T], _id: int, response_model: Type[V]) -> V | None:
    query = select(model).where(model.id == _id)
    result = (await session.execute(query)).scalar_one_or_none()

    if not result:
        return result
    return response_model.model_validate(result, from_attributes=True)


async def delete_by_id[T: Base](session: AsyncSession, model: Type[T], _id: int) -> None:
    stmp = delete(model).where(model.id == _id)
    await session.execute(stmp)
    await session.commit()


async def get_all[T: Base, V: BaseModel](session: AsyncSession, model: Type[T], response_model: Type[V], paging: PagingFilter | None = None, content_filter: BaseFilter | None = None) -> list[V]:
    query = select(model)
    if paging:
        query = paging(query)

    if content_filter:
        query = content_filter(query)

    result = await session.execute(query)
    return [response_model.model_validate(i, from_attributes=True) for i in result.scalars()]


async def get_by[T: Base, V: BaseModel](session: AsyncSession, model: Type[T], expression, response_model: Type[V], paging: PagingFilter | None = None):
    query = select(model).where(expression)
    if paging:
        query = paging(query)
    result = await session.execute(query)
    return [response_model.model_validate(i, from_attributes=True) for i in result.scalars()]


async def delete_by_ids[T: Base](session: AsyncSession, model: Type[T], ids: list[int]) -> None:
    stmp = delete(model).where(model.id.in_(ids))
    await session.execute(stmp)
    await session.commit()


async def update_by_id[T: Base, V: BaseModel](session: AsyncSession, model: Type[T], obj_id: int, data: V) -> None:
    stmp = (
        update(model)
        .values(**data.model_dump())
        .where(model.id == obj_id)
    )
    await session.execute(stmp)
    await session.commit()


