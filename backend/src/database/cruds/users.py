from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User
from src.schemas.users import UserOutWithHashedPassword


async def get_by_login(session: AsyncSession, email: str) -> UserOutWithHashedPassword:
    query = select(User).where(User.email == email)
    result = (await session.execute(query)).scalar_one_or_none()
    if not result:
        return None
    return UserOutWithHashedPassword.model_validate(result, from_attributes=True)
