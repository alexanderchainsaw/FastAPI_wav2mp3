from fastapi import APIRouter, Depends
from .service import create_user
from .models import UserCreate
from wav2mp3.database.core import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
users_router = APIRouter()


@users_router.post("")
async def create(session: Annotated[AsyncSession, Depends(get_db)], user_create: UserCreate):
    user = await create_user(session, user_create)
    return JSONResponse(status_code=201, content={
        "user_id": user.id,
        "token": user.token
    })

