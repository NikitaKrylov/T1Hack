from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import Sprint, Entity


async def get_entity_id_with_sprints(session: AsyncSession):
    query = (
        select(
            Sprint.name,
            Sprint.sprint_status,
            Sprint.started_at,
            Sprint.finished_at,
            Entity.entity_id
        )
        .select_from(Entity)
        .join(Sprint, Entity.sprint_id == Sprint.id)
    )
    result = await session.execute(query)
    return result.all()

