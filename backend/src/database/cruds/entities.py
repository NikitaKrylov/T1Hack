from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Entity


async def create_blank_entities(session: AsyncSession, sprint_id: int, entity_ids: list[int]) -> None:
    new_blank_entities = [Entity(sprint_id=sprint_id, entity_id=entity_id) for entity_id in entity_ids]
    session.add_all(new_blank_entities)
    await session.commit()

