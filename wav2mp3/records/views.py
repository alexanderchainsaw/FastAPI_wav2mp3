from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.core import get_db
from ..users.models import User
from ..users.service import validate_credentials
from .models import RecordCreate
from .service import create_record, get_record
from .utils import construct_download_link

records_router = APIRouter()


@records_router.post("")
async def create(
    session: Annotated[AsyncSession, Depends(get_db)],
    record_create: RecordCreate = Depends(RecordCreate),
    user: User = Depends(validate_credentials),
):
    created = await create_record(session, wav_file=record_create.wav_file, user=user)
    return JSONResponse(
        status_code=201,
        content={
            "download_link": construct_download_link(
                record_id=created.id, user_id=created.user_id
            )
        },
    )


@records_router.get("")
async def get(
    session: Annotated[AsyncSession, Depends(get_db)],
    id: str,
    user: User = Depends(validate_credentials),
):
    record = await get_record(session, id, user.id)
    return FileResponse(
        path=record.path_to_mp3,
        media_type="audio/mpeg",
        filename=record.path_to_mp3.rsplit("/", 1)[-1],
        status_code=200,
    )
