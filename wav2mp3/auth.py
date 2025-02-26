from fastapi import Depends, Header, Query
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .database.core import get_db
from .users.models import User


async def validate_credentials(
    user_id: str = Query(..., title="user id"),
    token: str = Header(..., alias="token", title="auth token given on registration"),
    session: AsyncSession = Depends(get_db),
) -> User | None:
    user = await session.get(User, user_id)
    if not user or user.token != token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
