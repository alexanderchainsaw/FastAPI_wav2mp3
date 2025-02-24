from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.core import get_db
from ..users.models import User, UserCreate


async def validate_credentials(
    session: Annotated[AsyncSession, Depends(get_db)], user_id: str, token: str
) -> User | None:
    user = await session.get(User, user_id)
    if not user or user.token != token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    user = User(id=str(uuid4()), token=str(uuid4()), name=user_create.name)
    session.add(user)
    return user
