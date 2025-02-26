from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from ..users.models import User, UserCreate


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    user = User(id=str(uuid4()), token=str(uuid4()), name=user_create.name)
    session.add(user)
    return user
