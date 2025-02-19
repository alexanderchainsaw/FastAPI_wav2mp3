from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.core import get_db
from ..users.service import validate_credentials
from .models import RecordCreate
from .service import create_record, get_record
from .utils import construct_download_link

records_router = APIRouter()


@records_router.post("")
async def create(
    session: Annotated[AsyncSession, Depends(get_db)],
    record_create: RecordCreate = Depends(RecordCreate),
):
    await validate_credentials(
        session, user_id=str(record_create.user_id), token=str(record_create.token)
    )
    created = await create_record(session, record_create)
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
    session: Annotated[AsyncSession, Depends(get_db)], record_id: str, user_id: str
):
    record = await get_record(session, record_id, user_id)
    return FileResponse(
        path=record.path_to_mp3,
        media_type="audio/mpeg",
        filename=record.path_to_mp3.rsplit("/", 1)[-1],
        status_code=200,
    )
