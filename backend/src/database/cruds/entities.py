from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Entity
from src.schemas.entities import EntityUpdate
from sqlalchemy import update
from src.database.cruds import base as base_cruds


async def create_blank_entities(session: AsyncSession, sprint_id: int, entity_ids: list[int]) -> None:
    new_blank_entities = [Entity(sprint_id=sprint_id, entity_id=entity_id) for entity_id in entity_ids]
    session.add_all(new_blank_entities)
    await session.commit()


async def update_entities_by_ids(session: AsyncSession, entities: list[EntityUpdate]) -> None:
    for entity in entities:
        entity_data = entity.model_dump()
        stmp = (
            update(Entity)
            .values(**entity_data)
            .where(Entity.id == entity.id)
        )
        await session.execute(stmp)

    await session.commit()


