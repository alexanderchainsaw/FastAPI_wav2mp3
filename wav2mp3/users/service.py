from wav2mp3.users.models import User, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from fastapi.exceptions import HTTPException


async def validate_credentials(session: AsyncSession, user_id: str, token: str) -> None:
    user = await session.get(User, user_id)
    if not user or user.token != token:
        raise HTTPException(status_code=401, detail="Invalid credentials")


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    user = User(id=str(uuid4()),
                token=str(uuid4()), name=user_create.name)
    session.add(user)
    return user



